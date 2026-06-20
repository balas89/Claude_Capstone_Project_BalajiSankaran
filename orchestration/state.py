from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List, TypedDict, Annotated
from microservices.schemas import (
    LoanApplication, ApplicantProfileResult, FinancialRiskResult,
    LoanDecisionResult, ComplianceResult
)
from operator import add


# LangGraph TypedDict for state management
class WorkflowState(TypedDict):
    """LangGraph-compatible state definition"""
    # Application data
    application: LoanApplication
    case_id: str

    # Agent results
    applicant_profile_result: Optional[ApplicantProfileResult]
    financial_risk_result: Optional[FinancialRiskResult]
    loan_decision_result: Optional[LoanDecisionResult]
    compliance_result: Optional[ComplianceResult]

    # Workflow state
    current_step: str
    errors: Annotated[List[str], add]
    processing_complete: bool

@dataclass
class ApplicationState:
    """Central state for loan application processing (legacy dataclass support)"""

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
        profile = (
            self.applicant_profile_result.model_dump()
            if self.applicant_profile_result
            else None
        )
        financial = (
            self.financial_risk_result.model_dump()
            if self.financial_risk_result
            else None
        )
        decision = (
            self.loan_decision_result.model_dump()
            if self.loan_decision_result
            else None
        )
        compliance = (
            self.compliance_result.model_dump()
            if self.compliance_result
            else None
        )
        return {
            "application": self.application.model_dump(),
            "case_id": self.case_id,
            "applicant_profile_result": profile,
            "financial_risk_result": financial,
            "loan_decision_result": decision,
            "compliance_result": compliance,
            "current_step": self.current_step,
            "errors": self.errors,
            "processing_complete": self.processing_complete,
        }

    @classmethod
    def from_workflow_state(cls, state: WorkflowState) -> "ApplicationState":
        """Convert WorkflowState to ApplicationState"""
        return cls(
            application=state["application"],
            case_id=state["case_id"],
            applicant_profile_result=state.get("applicant_profile_result"),
            financial_risk_result=state.get("financial_risk_result"),
            loan_decision_result=state.get("loan_decision_result"),
            compliance_result=state.get("compliance_result"),
            current_step=state.get("current_step", "start"),
            errors=state.get("errors", []),
            processing_complete=state.get("processing_complete", False),
        )

    def to_workflow_state(self) -> WorkflowState:
        """Convert ApplicationState to WorkflowState"""
        return {
            "application": self.application,
            "case_id": self.case_id,
            "applicant_profile_result": self.applicant_profile_result,
            "financial_risk_result": self.financial_risk_result,
            "loan_decision_result": self.loan_decision_result,
            "compliance_result": self.compliance_result,
            "current_step": self.current_step,
            "errors": self.errors,
            "processing_complete": self.processing_complete,
        }
