"""LangGraph Orchestration Workflow for Loan Application Processing"""
import asyncio
from datetime import datetime
from orchestration.state import ApplicationState
from agents.applicant_agent import create_applicant_agent
from agents.financial_risk_agent import create_financial_risk_agent
from agents.loan_decision_agent import create_loan_decision_agent
from agents.compliance_agent import create_compliance_agent
from utils.mock_data import generate_case_id
from microservices.schemas import LoanApplication, LoanDecisionResponse

class LoanApprovalWorkflow:
    """Orchestrates the loan approval workflow"""

    def __init__(self):
        self.applicant_agent = create_applicant_agent()
        self.financial_risk_agent = create_financial_risk_agent()
        self.loan_decision_agent = create_loan_decision_agent()
        self.compliance_agent = create_compliance_agent()

    async def process_application(self, application: LoanApplication) -> LoanDecisionResponse:
        """Execute full loan approval workflow"""

        # Initialize state
        state = ApplicationState(application=application)
        state.case_id = generate_case_id(application.applicant_id)

        try:
            # Step 1: Analyze applicant profile
            state.current_step = "analyzing_profile"
            state.applicant_profile_result = await self.applicant_agent.analyze(application)

            # Step 2: Analyze financial risk (parallel possible, but sequential for clarity)
            state.current_step = "analyzing_financial_risk"
            state.financial_risk_result = await self.financial_risk_agent.analyze(application)

            # Step 3: Make loan decision using Claude
            state.current_step = "synthesizing_decision"
            state.loan_decision_result = await self.loan_decision_agent.decide(
                application,
                state.applicant_profile_result,
                state.financial_risk_result,
            )

            # Step 4: Execute compliance and send notifications
            state.current_step = "executing_compliance"
            state.compliance_result = await self.compliance_agent.execute(
                application,
                state.loan_decision_result,
                state.applicant_profile_result,
                state.financial_risk_result,
            )

            state.processing_complete = True
            state.current_step = "completed"

        except Exception as e:
            state.errors.append(str(e))
            state.current_step = "error"

        # Build final response
        return self._build_response(state)

    def _build_response(self, state: ApplicationState) -> LoanDecisionResponse:
        """Build final response from state"""
        if state.errors:
            return LoanDecisionResponse(
                case_id=state.case_id,
                applicant_id=state.application.applicant_id,
                decision="Requires Manual Review",
                risk_score=0.5,
                confidence=0.0,
                factors=state.errors,
                explanation=f"Error during processing: {', '.join(state.errors)}",
                profile_analysis=state.applicant_profile_result or {},
                financial_analysis=state.financial_risk_result or {},
                compliance_status=state.compliance_result or {},
                timestamp=datetime.now().isoformat(),
            )

        return LoanDecisionResponse(
            case_id=state.case_id,
            applicant_id=state.application.applicant_id,
            decision=state.loan_decision_result.decision,
            risk_score=state.loan_decision_result.risk_score,
            confidence=state.loan_decision_result.confidence_level,
            factors=state.loan_decision_result.key_factors,
            explanation=state.loan_decision_result.explanation,
            profile_analysis=state.applicant_profile_result,
            financial_analysis=state.financial_risk_result,
            compliance_status=state.compliance_result,
            timestamp=datetime.now().isoformat(),
        )

def create_workflow():
    """Factory function to create workflow"""
    return LoanApprovalWorkflow()
