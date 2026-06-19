"""MCP Server: Decision Synthesis - Uses Claude API"""
from fastapi import FastAPI
from pydantic import BaseModel
from anthropic import Anthropic
from utils.config import ANTHROPIC_API_KEY, MODEL_NAME

app = FastAPI(title="Decision Synthesis MCP Server")
client = Anthropic(api_key=ANTHROPIC_API_KEY)

class DecisionRequest(BaseModel):
    applicant_id: str
    profile_analysis: dict
    financial_analysis: dict
    loan_details: dict

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "decision_synthesis"}

@app.post("/synthesize_decision")
async def synthesize_decision(request: DecisionRequest):
    """Use Claude to synthesize final loan decision"""

    prompt = f"""
You are an expert loan officer analyzing a loan application. Based on the following analysis, provide a final decision.

APPLICANT PROFILE ANALYSIS:
- Income Stability Score: {request['profile_analysis'].get('income_stability_score', 0)}
- Employment Risk: {request['profile_analysis'].get('employment_risk', 'Unknown')}
- Credit Score: {request['profile_analysis']['credit_history_summary']['credit_score']}
- Payment History: {request['profile_analysis']['credit_history_summary']['payment_history']}
- Late Payments (6m): {request['profile_analysis']['credit_history_summary']['late_payments_6m']}
- Collections: {request['profile_analysis']['credit_history_summary']['collections']}
- Completeness Flags: {', '.join(request['profile_analysis'].get('completeness_flags', []))}

FINANCIAL RISK ANALYSIS:
- Debt-to-Income Ratio: {request['financial_analysis'].get('dti_ratio', 0)}
- Credit Risk Level: {request['financial_analysis'].get('credit_risk_level', 'Unknown')}
- Loan Amount Risk: {request['financial_analysis'].get('loan_amount_risk', 'Unknown')}
- Anomalies: {', '.join(request['financial_analysis'].get('anomalies', []))}

LOAN DETAILS:
- Loan Amount: ${request['loan_details'].get('loan_amount', 0):,.2f}
- Tenure: {request['loan_details'].get('tenure_months', 0)} months
- Applicant Income: ${request['loan_details'].get('income', 0):,.2f}
- Existing Liabilities: ${request['loan_details'].get('existing_liabilities', 0):,.2f}

Provide your decision in the following JSON format:
{{
    "decision": "Approve" or "Reject" or "Requires Manual Review",
    "confidence": 0.0 to 1.0,
    "risk_score": 0.0 to 1.0,
    "key_factors": ["factor1", "factor2", "factor3"],
    "explanation": "Brief explanation of the decision"
}}

Be thorough but concise. Consider both positive and negative factors.
"""

    response = client.messages.create(
        model=MODEL_NAME,
        max_tokens=500,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    import json
    response_text = response.content[0].text

    try:
        start_idx = response_text.find('{')
        end_idx = response_text.rfind('}') + 1
        json_str = response_text[start_idx:end_idx]
        decision_data = json.loads(json_str)
    except (json.JSONDecodeError, ValueError):
        decision_data = {
            "decision": "Requires Manual Review",
            "confidence": 0.5,
            "risk_score": 0.5,
            "key_factors": ["LLM analysis required"],
            "explanation": response_text[:200]
        }

    return {
        "applicant_id": request["applicant_id"],
        "decision": decision_data.get("decision", "Requires Manual Review"),
        "confidence": decision_data.get("confidence", 0.5),
        "risk_score": decision_data.get("risk_score", 0.5),
        "key_factors": decision_data.get("key_factors", []),
        "explanation": decision_data.get("explanation", ""),
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
