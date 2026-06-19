"""Agent: Compliance & Action Orchestrator"""
import requests
from utils.config import NOTIFICATION_SYSTEM_URL
from microservices.schemas import (
    ComplianceResult, LoanApplication, LoanDecisionResult,
    ApplicantProfileResult, FinancialRiskResult
)

class ComplianceAgent:
    """Executes compliance checks and sends notifications via MCP NotificationSystem"""

    def __init__(self):
        self.service_url = NOTIFICATION_SYSTEM_URL

    async def execute(
        self,
        application: LoanApplication,
        decision_result: LoanDecisionResult,
        profile_analysis: ApplicantProfileResult,
        financial_analysis: FinancialRiskResult,
    ) -> ComplianceResult:
        """Execute compliance checks and send notifications"""
        try:
            response = requests.post(
                f"{self.service_url}/execute_compliance_and_notify",
                json={
                    "applicant_id": application.applicant_id,
                    "location": application.location,
                    "decision": decision_result.decision,
                    "risk_factors": {
                        "risk_score": decision_result.risk_score,
                        "dti_ratio": financial_analysis.dti_ratio,
                        "credit_risk": financial_analysis.credit_risk_level,
                    },
                    "profile_analysis": profile_analysis.model_dump(),
                }
            )
            response.raise_for_status()
            data = response.json()

            return ComplianceResult(
                applicant_id=application.applicant_id,
                action_taken=data.get("action_taken", ""),
                notification_sent=data.get("notification_sent", False),
                case_id=data.get("case_id", ""),
                timestamp=data.get("timestamp", ""),
                summary=data.get("summary", ""),
            )
        except Exception as e:
            raise RuntimeError(f"Compliance Agent failed: {str(e)}")

def create_compliance_agent():
    """Factory function to create compliance agent"""
    return ComplianceAgent()
