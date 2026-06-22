"""MCP Server: Decision Synthesis - Uses Business Rules & Claude API"""
from fastapi import FastAPI
from pydantic import BaseModel
from anthropic import Anthropic
from utils.config import ANTHROPIC_API_KEY, MODEL_NAME
from utils.decision_rules import LoanDecisionRules

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
    """
    Make loan decision using BUSINESS RULES, not LLM confidence level.

    Decision criteria:
    - Hard rejection: DTI >= 50%, Credit score < 600, severe anomalies
    - Approval: Good financial metrics (DTI < 43%, Credit >= 650)
    - Manual Review: Mixed signals requiring human judgment
    """

    # Extract key metrics
    dti_ratio = request['financial_analysis'].get('dti_ratio', 0.5)
    credit_score = request['profile_analysis']['credit_history_summary']['credit_score']
    loan_to_income = request['financial_analysis'].get('loan_to_income_ratio', 3.0)
    income_stability = request['profile_analysis'].get('income_stability_score', 0.5)
    employment_risk = request['profile_analysis'].get('employment_risk', 'Medium')
    anomalies = request['financial_analysis'].get('anomalies', [])
    completeness_flags = request['profile_analysis'].get('completeness_flags', [])

    # Apply business rules for decision
    decision, risk_score, reasoning = LoanDecisionRules.make_decision(
        dti_ratio=dti_ratio,
        credit_score=credit_score,
        loan_to_income=loan_to_income,
        income_stability=income_stability,
        employment_risk=employment_risk,
        anomalies=anomalies,
        completeness_flags=completeness_flags
    )

    # Get enhanced explanation from Claude (for transparency, not for decision)
    prompt = f"""
You are a loan officer providing additional context for a loan decision that was made based on business rules.

APPLICATION SUMMARY:
- Credit Score: {credit_score}
- DTI Ratio: {dti_ratio:.2f}
- Loan-to-Income: {loan_to_income:.2f}x
- Employment Risk: {employment_risk}
- Anomalies: {len(anomalies)} detected
- Decision: {decision}

Provide 2-3 key factors that support this decision based on BUSINESS CRITERIA (not confidence).
Focus on financial metrics, not LLM confidence levels.
Format as a simple explanation (no JSON).
"""

    try:
        response = client.messages.create(
            model=MODEL_NAME,
            max_tokens=300,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        enhanced_explanation = response.content[0].text
    except:
        enhanced_explanation = reasoning

    # Extract key factors from business rules
    key_factors = []
    if dti_ratio < 0.30:
        key_factors.append("Excellent debt-to-income ratio")
    elif dti_ratio < 0.43:
        key_factors.append("Good debt-to-income ratio")
    elif dti_ratio >= 0.50:
        key_factors.append("High debt-to-income ratio - risk factor")

    if credit_score >= 750:
        key_factors.append("Excellent credit history")
    elif credit_score >= 700:
        key_factors.append("Very good credit history")
    elif credit_score < 650:
        key_factors.append("Fair credit history - needs review")

    if employment_risk == "Low":
        key_factors.append("Stable employment history")
    elif employment_risk == "High":
        key_factors.append("Employment risk - needs review")

    if anomalies:
        key_factors.append(f"Anomalies detected: {', '.join(anomalies[:2])}")

    return {
        "applicant_id": request["applicant_id"],
        "decision": decision,  # Based on BUSINESS RULES, not confidence
        "risk_score": risk_score,  # Calculated from financial metrics
        "confidence": 0.85,  # Always high because decision is rule-based, not LLM-based
        "decision_basis": "BUSINESS RULES (DTI, Credit Score, Financial Metrics)",
        "key_factors": key_factors[:3],  # Top 3 factors
        "explanation": f"{reasoning}\n\nAdditional Context:\n{enhanced_explanation}",
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
