"""True MCP Server: Risk Rules Database using FastMCP"""
import asyncio
from mcp.server import Server
from pydantic import BaseModel
from utils.mock_data import MockComplianceRulesDB


class AnalyzeRiskRequest(BaseModel):
    """Request model for financial risk analysis"""
    applicant_id: str
    income: float
    employment_years: int
    credit_score: int
    loan_amount: float
    existing_debt: float = 0.0


# Create MCP Server
server = Server("risk-rules-db-mcp")


@server.list_resources()
async def list_resources():
    """List available resources"""
    return [
        {
            "uri": "risk-rules://resources/analysis",
            "name": "Risk Analysis Engine",
            "description": "Analyze financial risk and calculate risk metrics",
            "mimeType": "application/json"
        }
    ]


@server.read_resource()
async def read_resource(uri: str):
    """Read a specific resource"""
    if uri == "risk-rules://resources/analysis":
        return "Financial Risk Analysis Service"
    raise ValueError(f"Unknown resource: {uri}")


@server.list_tools()
async def list_tools():
    """List available tools"""
    return [
        {
            "name": "analyze_financial_risk",
            "description": "Analyze financial risk including DTI ratio, credit risk level, loan amount risk, and anomaly detection",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "applicant_id": {
                        "type": "string",
                        "description": "Unique applicant identifier"
                    },
                    "income": {
                        "type": "number",
                        "description": "Annual income in dollars"
                    },
                    "employment_years": {
                        "type": "integer",
                        "description": "Years of employment"
                    },
                    "credit_score": {
                        "type": "integer",
                        "description": "Applicant credit score"
                    },
                    "loan_amount": {
                        "type": "number",
                        "description": "Requested loan amount in dollars"
                    },
                    "existing_debt": {
                        "type": "number",
                        "description": "Existing monthly debt obligations",
                        "default": 0.0
                    }
                },
                "required": ["applicant_id", "income", "employment_years", "credit_score", "loan_amount"]
            }
        }
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict):
    """Execute a tool"""
    if name != "analyze_financial_risk":
        raise ValueError(f"Unknown tool: {name}")

    # Parse request
    request = AnalyzeRiskRequest(**arguments)

    # Calculate DTI Ratio
    monthly_income = request.income / 12
    monthly_loan_payment = (request.loan_amount * 0.006) / (1 - (1 + 0.006) ** -360)
    total_monthly_debt = request.existing_debt + monthly_loan_payment
    dti_ratio = total_monthly_debt / monthly_income if monthly_income > 0 else 1.0

    # Determine credit risk level (4 levels)
    if request.credit_score >= 750:
        credit_risk_level = "Low"
        credit_risk_score = 0.2
    elif request.credit_score >= 700:
        credit_risk_level = "Medium"
        credit_risk_score = 0.5
    elif request.credit_score >= 650:
        credit_risk_level = "High"
        credit_risk_score = 0.7
    else:
        credit_risk_level = "Very High"
        credit_risk_score = 0.9

    # Assess loan amount risk
    loan_to_income_ratio = request.loan_amount / request.income if request.income > 0 else 0
    if loan_to_income_ratio < 2.0:
        loan_amount_risk = "Low"
    elif loan_to_income_ratio < 3.0:
        loan_amount_risk = "Medium"
    elif loan_to_income_ratio < 4.0:
        loan_amount_risk = "High"
    else:
        loan_amount_risk = "Very High"

    # Detect 7 types of anomalies
    anomalies = []

    # 1. High DTI with low credit score
    if dti_ratio > 0.43 and request.credit_score < 700:
        anomalies.append("High DTI with low credit score")

    # 2. Recent employment with high debt
    if request.employment_years < 2 and dti_ratio > 0.40:
        anomalies.append("Recent employment with high debt obligations")

    # 3. Income inconsistency (simulated)
    if request.income < 30000 and request.loan_amount > 200000:
        anomalies.append("Income-to-loan-amount inconsistency")

    # 4. Multiple recent inquiries (simulated)
    if request.credit_score < 650:
        anomalies.append("Multiple recent credit inquiries indicated by low score")

    # 5. Recent bankruptcies/collections (simulated by very low score)
    if request.credit_score < 600:
        anomalies.append("Recent negative credit events")

    # 6. Mismatched employment/income
    if request.employment_years > 10 and request.income < 40000:
        anomalies.append("Long employment history with low income")

    # 7. Application inconsistencies
    if dti_ratio > 0.50 and loan_to_income_ratio > 3.5:
        anomalies.append("High debt burden and high loan-to-income ratio")

    # Generate reasoning
    reasoning = []
    reasoning.append(f"DTI ratio: {dti_ratio:.2f} ({'Acceptable' if dti_ratio <= 0.43 else 'High'})")
    reasoning.append(f"Credit risk level: {credit_risk_level} (score: {request.credit_score})")
    reasoning.append(f"Loan-to-income ratio: {loan_to_income_ratio:.2f}x")
    reasoning.append(f"Employment stability: {request.employment_years} years")
    if anomalies:
        reasoning.append(f"Anomalies detected: {len(anomalies)}")

    return {
        "applicant_id": request.applicant_id,
        "dti_ratio": round(dti_ratio, 4),
        "credit_risk_level": credit_risk_level,
        "credit_risk_score": credit_risk_score,
        "loan_amount_risk": loan_amount_risk,
        "loan_to_income_ratio": round(loan_to_income_ratio, 2),
        "anomalies": anomalies,
        "anomaly_count": len(anomalies),
        "reasoning": reasoning,
        "risk_assessment": "Approve" if dti_ratio <= 0.43 and credit_risk_level in ["Low", "Medium"] else "Review"
    }


async def main():
    """Main entry point for MCP server"""
    async with server:
        await server.wait_for_shutdown()


if __name__ == "__main__":
    asyncio.run(main())
