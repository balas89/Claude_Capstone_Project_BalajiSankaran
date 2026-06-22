"""True MCP Server: Decision Synthesis using FastMCP"""
import asyncio
import json
import os
from mcp.server import Server
from pydantic import BaseModel
from anthropic import Anthropic


class SynthesizeDecisionRequest(BaseModel):
    """Request model for decision synthesis"""
    applicant_id: str
    applicant_profile: dict
    financial_risk: dict


# Create MCP Server
server = Server("decision-synthesis-mcp")

# Initialize Anthropic client
client = Anthropic()


@server.list_resources()
async def list_resources():
    """List available resources"""
    return [
        {
            "uri": "decision-synthesis://resources/claude",
            "name": "Claude Decision Engine",
            "description": "LLM-powered decision synthesis using Claude Sonnet",
            "mimeType": "application/json"
        }
    ]


@server.read_resource()
async def read_resource(uri: str):
    """Read a specific resource"""
    if uri == "decision-synthesis://resources/claude":
        return "Claude Sonnet Decision Synthesis Service"
    raise ValueError(f"Unknown resource: {uri}")


@server.list_tools()
async def list_tools():
    """List available tools"""
    return [
        {
            "name": "synthesize_decision",
            "description": "Synthesize loan decision using Claude AI by analyzing applicant profile and financial risk",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "applicant_id": {
                        "type": "string",
                        "description": "Unique applicant identifier"
                    },
                    "applicant_profile": {
                        "type": "object",
                        "description": "Applicant profile analysis results"
                    },
                    "financial_risk": {
                        "type": "object",
                        "description": "Financial risk analysis results"
                    }
                },
                "required": ["applicant_id", "applicant_profile", "financial_risk"]
            }
        }
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict):
    """Execute a tool"""
    if name != "synthesize_decision":
        raise ValueError(f"Unknown tool: {name}")

    # Parse request
    request = SynthesizeDecisionRequest(**arguments)

    # Build comprehensive prompt for Claude
    prompt = f"""You are an expert loan approval decision synthesizer. Analyze the following applicant information and provide a loan decision.

APPLICANT PROFILE:
- Income Stability Score: {request.applicant_profile.get('income_stability_score', 0):.2f}
- Employment Risk: {request.applicant_profile.get('employment_risk', 'Unknown')}
- Credit History: {json.dumps(request.applicant_profile.get('credit_history', {}), indent=2)}
- Completeness Flags: {', '.join(request.applicant_profile.get('completeness_flags', [])) or 'None'}

FINANCIAL RISK ANALYSIS:
- DTI Ratio: {request.financial_risk.get('dti_ratio', 0):.4f}
- Credit Risk Level: {request.financial_risk.get('credit_risk_level', 'Unknown')}
- Loan Amount Risk: {request.financial_risk.get('loan_amount_risk', 'Unknown')}
- Loan-to-Income Ratio: {request.financial_risk.get('loan_to_income_ratio', 0):.2f}x
- Anomalies Detected: {', '.join(request.financial_risk.get('anomalies', [])) or 'None'}
- Risk Assessment Reasoning:
  {chr(10).join('  - ' + r for r in request.financial_risk.get('reasoning', []))}

DECISION CRITERIA:
- DTI threshold (recommended): 0.43
- DTI threshold (critical): 0.50
- Minimum credit score for approval: 650
- Target loan-to-income ratio: Below 3.0x

Based on this information, provide:
1. A loan decision (Approve, Reject, or Requires Manual Review)
2. A risk score (0.0 to 1.0, where 0 is lowest risk)
3. A confidence level (0.0 to 1.0)
4. 3-5 key factors influencing the decision
5. A brief explanation (2-3 sentences)

Respond in JSON format only with keys: decision, risk_score, confidence_level, key_factors, explanation"""

    try:
        # Call Claude API
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        # Parse response
        response_text = message.content[0].text

        # Extract JSON from response
        try:
            # Try to find JSON in the response
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            if start_idx >= 0 and end_idx > start_idx:
                json_str = response_text[start_idx:end_idx]
                decision_data = json.loads(json_str)
            else:
                decision_data = json.loads(response_text)
        except json.JSONDecodeError:
            # Fallback if JSON parsing fails
            decision_data = {
                "decision": "Requires Manual Review",
                "risk_score": 0.5,
                "confidence_level": 0.6,
                "key_factors": ["Unable to parse LLM response", "Manual review required"],
                "explanation": "The system encountered an error processing the decision. Manual review is recommended."
            }

        return {
            "applicant_id": request.applicant_id,
            "decision": decision_data.get("decision", "Requires Manual Review"),
            "risk_score": float(decision_data.get("risk_score", 0.5)),
            "confidence_level": float(decision_data.get("confidence_level", 0.5)),
            "key_factors": decision_data.get("key_factors", []),
            "explanation": decision_data.get("explanation", "")
        }

    except Exception as e:
        # Error handling
        return {
            "applicant_id": request.applicant_id,
            "decision": "Requires Manual Review",
            "risk_score": 0.5,
            "confidence_level": 0.3,
            "key_factors": [f"System error: {str(e)}", "Manual review required"],
            "explanation": f"An error occurred during decision synthesis: {str(e)}"
        }


async def main():
    """Main entry point for MCP server"""
    async with server:
        await server.wait_for_shutdown()


if __name__ == "__main__":
    asyncio.run(main())
