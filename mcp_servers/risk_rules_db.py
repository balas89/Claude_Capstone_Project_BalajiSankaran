"""MCP Server: Financial Risk Rules Database"""
from fastapi import FastAPI
from pydantic import BaseModel
from utils.config import (
    RECOMMENDED_DTI_THRESHOLD, CRITICAL_DTI_THRESHOLD,
    MIN_INCOME, MAX_LOAN_AMOUNT, MIN_CREDIT_SCORE
)

app = FastAPI(title="Risk Rules DB MCP Server")

class FinancialRiskRequest(BaseModel):
    applicant_id: str
    income: float
    credit_score: int
    loan_amount: float
    tenure_months: int
    existing_liabilities: float

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "risk_rules_db"}

@app.post("/analyze_financial_risk")
async def analyze_financial_risk(request: FinancialRiskRequest):
    """Analyze financial risk based on rules"""

    # Calculate monthly income and obligations
    monthly_income = request.income / 12
    monthly_loan_payment = (request.loan_amount / request.tenure_months) if request.tenure_months > 0 else 0
    monthly_existing_obligations = request.existing_liabilities / 12

    # Calculate debt-to-income ratio
    total_monthly_obligations = monthly_loan_payment + monthly_existing_obligations
    dti_ratio = total_monthly_obligations / monthly_income if monthly_income > 0 else 1.0

    # Determine credit risk level
    if request.credit_score >= 750:
        credit_risk_level = "Low"
    elif request.credit_score >= 650:
        credit_risk_level = "Medium"
    elif request.credit_score >= MIN_CREDIT_SCORE:
        credit_risk_level = "High"
    else:
        credit_risk_level = "Critical"

    # Assess loan amount risk
    if request.loan_amount > MAX_LOAN_AMOUNT:
        loan_amount_risk = "Excessive"
    elif request.loan_amount > request.income * 5:
        loan_amount_risk = "High"
    elif request.loan_amount > request.income * 2:
        loan_amount_risk = "Medium"
    else:
        loan_amount_risk = "Low"

    # Detect anomalies
    anomalies = []
    if request.income < MIN_INCOME:
        anomalies.append("Income below minimum threshold")
    if dti_ratio > CRITICAL_DTI_THRESHOLD:
        anomalies.append("DTI ratio critically high")
    elif dti_ratio > RECOMMENDED_DTI_THRESHOLD:
        anomalies.append("DTI ratio above recommended threshold")
    if request.credit_score < 600:
        anomalies.append("Credit score below acceptable range")
    if request.loan_amount > request.income * 10:
        anomalies.append("Loan amount significantly exceeds income")
    if request.tenure_months < 12:
        anomalies.append("Loan tenure too short")
    if request.tenure_months > 360:
        anomalies.append("Loan tenure excessive")

    reasoning = f"DTI: {dti_ratio:.2f}, Credit Risk: {credit_risk_level}, Loan Risk: {loan_amount_risk}, Anomalies: {len(anomalies)}"

    return {
        "applicant_id": request.applicant_id,
        "dti_ratio": round(dti_ratio, 3),
        "credit_risk_level": credit_risk_level,
        "loan_amount_risk": loan_amount_risk,
        "anomalies": anomalies,
        "reasoning": reasoning,
        "monthly_income": round(monthly_income, 2),
        "monthly_obligations": round(total_monthly_obligations, 2),
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
