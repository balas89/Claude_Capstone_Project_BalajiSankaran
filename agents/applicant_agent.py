"""Agent: Applicant Profile Analysis"""
import requests
from utils.config import APPLICANT_DB_URL
from microservices.schemas import ApplicantProfileResult, LoanApplication

class ApplicantProfileAgent:
    """Analyzes applicant profile using MCP ApplicantDB"""

    def __init__(self):
        self.service_url = APPLICANT_DB_URL

    async def analyze(self, application: LoanApplication) -> ApplicantProfileResult:
        """Analyze applicant profile"""
        try:
            response = requests.post(
                f"{self.service_url}/get_applicant_profile",
                json={
                    "applicant_id": application.applicant_id,
                    "age": application.age,
                    "income": application.income,
                    "employment_type": application.employment_type,
                    "credit_score": application.credit_score,
                }
            )
            response.raise_for_status()
            data = response.json()

            return ApplicantProfileResult(
                applicant_id=application.applicant_id,
                income_stability_score=data.get("income_stability_score", 0),
                employment_risk=data.get("employment_risk", "Unknown"),
                credit_history_summary=data.get("credit_history_summary", {}),
                completeness_flags=data.get("completeness_flags", []),
            )
        except Exception as e:
            raise RuntimeError(f"Applicant Profile Agent failed: {str(e)}")

def create_applicant_agent():
    """Factory function to create applicant agent"""
    return ApplicantProfileAgent()
