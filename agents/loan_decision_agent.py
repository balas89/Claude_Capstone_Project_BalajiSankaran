"""Agent: Loan Decision - LLM-Powered"""
import requests
from utils.config import DECISION_SYNTHESIS_URL
from microservices.schemas import (
    LoanDecisionResult, LoanApplication, ApplicantProfileResult,
    FinancialRiskResult
)

class LoanDecisionAgent:
    """Synthesizes final loan decision using Claude via MCP DecisionSynthesis"""

    def __init__(self):
        self.service_url = DECISION_SYNTHESIS_URL

    async def decide(
        self,
        application: LoanApplication,
        profile_analysis: ApplicantProfileResult,
        financial_analysis: FinancialRiskResult,
    ) -> LoanDecisionResult:
        """Make final loan decision"""
        try:
            response = requests.post(
                f"{self.service_url}/synthesize_decision",
                json={
                    "applicant_id": application.applicant_id,
                    "profile_analysis": profile_analysis.model_dump(),
                    "financial_analysis": financial_analysis.model_dump(),
                    "loan_details": {
                        "loan_amount": application.loan_amount,
                        "tenure_months": application.tenure_months,
                        "income": application.income,
                        "existing_liabilities": application.existing_liabilities,
                    }
                }
            )
            response.raise_for_status()
            data = response.json()

            return LoanDecisionResult(
                applicant_id=application.applicant_id,
                decision=data.get("decision", "Requires Manual Review"),
                risk_score=data.get("risk_score", 0.5),
                confidence_level=data.get("confidence", 0.5),
                key_factors=data.get("key_factors", []),
                explanation=data.get("explanation", ""),
            )
        except Exception as e:
            raise RuntimeError(f"Loan Decision Agent failed: {str(e)}")

def create_loan_decision_agent():
    """Factory function to create loan decision agent"""
    return LoanDecisionAgent()
