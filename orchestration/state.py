from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List
from microservices.schemas import (
    LoanApplication, ApplicantProfileResult, FinancialRiskResult,
    LoanDecisionResult, ComplianceResult
)

@dataclass
class ApplicationState:
    """Central state for loan application processing"""

    # Application data
    application: LoanApplication
    case_id: str = ""

    # Agent results
    applicant_profile_result: Optional[ApplicantProfileResult] = None
    financial_risk_result: Optional[FinancialRiskResult] = None
    loan_decision_result: Optional[LoanDecisionResult] = None
    compliance_result: Optional[ComplianceResult] = None

    # Workflow state
    current_step: str = "start"
    errors: List[str] = field(default_factory=list)
    processing_complete: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Convert state to dictionary for serialization"""
        return {
            "application": self.application.model_dump(),
            "case_id": self.case_id,
            "applicant_profile_result": self.applicant_profile_result.model_dump() if self.applicant_profile_result else None,
            "financial_risk_result": self.financial_risk_result.model_dump() if self.financial_risk_result else None,
            "loan_decision_result": self.loan_decision_result.model_dump() if self.loan_decision_result else None,
            "compliance_result": self.compliance_result.model_dump() if self.compliance_result else None,
            "current_step": self.current_step,
            "errors": self.errors,
            "processing_complete": self.processing_complete,
        }
