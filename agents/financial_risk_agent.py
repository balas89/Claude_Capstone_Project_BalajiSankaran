"""Agent: Financial Risk Analysis"""
import requests
from utils.config import RISK_RULES_DB_URL
from microservices.schemas import FinancialRiskResult, LoanApplication

class FinancialRiskAgent:
    """Analyzes financial risk using MCP RiskRulesDB"""

    def __init__(self):
        self.service_url = RISK_RULES_DB_URL

    async def analyze(self, application: LoanApplication) -> FinancialRiskResult:
        """Analyze financial risk"""
        try:
            response = requests.post(
                f"{self.service_url}/analyze_financial_risk",
                json={
                    "applicant_id": application.applicant_id,
                    "income": application.income,
                    "credit_score": application.credit_score,
                    "loan_amount": application.loan_amount,
                    "tenure_months": application.tenure_months,
                    "existing_liabilities": application.existing_liabilities,
                }
            )
            response.raise_for_status()
            data = response.json()

            return FinancialRiskResult(
                applicant_id=application.applicant_id,
                dti_ratio=data.get("dti_ratio", 0),
                credit_risk_level=data.get("credit_risk_level", "Unknown"),
                loan_amount_risk=data.get("loan_amount_risk", "Unknown"),
                anomalies=data.get("anomalies", []),
                reasoning=data.get("reasoning", ""),
            )
        except Exception as e:
            raise RuntimeError(f"Financial Risk Agent failed: {str(e)}")

def create_financial_risk_agent():
    """Factory function to create financial risk agent"""
    return FinancialRiskAgent()
