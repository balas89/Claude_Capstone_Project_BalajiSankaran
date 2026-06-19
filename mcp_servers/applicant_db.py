"""MCP Server: Applicant Profile Database"""
from fastapi import FastAPI
from pydantic import BaseModel
from utils.mock_data import MockCreditHistoryDB, MockEmploymentDB

app = FastAPI(title="Applicant DB MCP Server")

class GetProfileRequest(BaseModel):
    applicant_id: str
    age: int
    income: float
    employment_type: str
    credit_score: int

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "applicant_db"}

@app.post("/get_applicant_profile")
async def get_applicant_profile(request: GetProfileRequest):
    """Analyze applicant profile and return assessment"""

    credit_history = MockCreditHistoryDB.get_credit_history(request.applicant_id)
    employment_info = MockEmploymentDB.verify_employment(
        request.applicant_id, request.employment_type
    )

    # Calculate income stability score (0-1)
    income_stability = 0.0
    if employment_info["verified"]:
        years_employed = employment_info["years_employed"]
        income_stability = min(1.0, years_employed / 10.0 + 0.2)
    else:
        income_stability = 0.2

    # Determine employment risk
    if not employment_info["verified"]:
        employment_risk = "High"
    elif employment_info["job_stability_score"] < 0.5:
        employment_risk = "Medium"
    else:
        employment_risk = "Low"

    # Completeness flags
    completeness_flags = []
    if request.income < 20000:
        completeness_flags.append("Income below minimum threshold")
    if request.age < 21:
        completeness_flags.append("Applicant under 21")
    if credit_history["collections"] > 0:
        completeness_flags.append("Collections account detected")
    if credit_history["late_payments_12m"] > 3:
        completeness_flags.append("Multiple recent late payments")

    return {
        "applicant_id": request.applicant_id,
        "income_stability_score": income_stability,
        "employment_risk": employment_risk,
        "credit_history_summary": {
            "credit_score": credit_history["credit_score"],
            "payment_history": credit_history["payment_history"],
            "accounts_count": credit_history["accounts_count"],
            "late_payments_6m": credit_history["late_payments_6m"],
            "late_payments_12m": credit_history["late_payments_12m"],
            "collections": credit_history["collections"],
            "inquiries_6m": credit_history["inquiries_6m"],
        },
        "employment_verified": employment_info["verified"],
        "years_employed": employment_info["years_employed"],
        "completeness_flags": completeness_flags,
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
