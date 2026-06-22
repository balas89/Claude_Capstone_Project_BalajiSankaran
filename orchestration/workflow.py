"""LangGraph Orchestration Workflow for Loan Application Processing"""
import asyncio
from asyncio import run
from datetime import datetime
from langgraph.graph import StateGraph, END
from orchestration.state import ApplicationState, WorkflowState
from agents.applicant_agent import create_applicant_agent
from agents.financial_risk_agent import create_financial_risk_agent
from agents.loan_decision_agent import create_loan_decision_agent
from agents.compliance_agent import create_compliance_agent
from utils.mock_data import generate_case_id
from microservices.schemas import (
    LoanApplication, LoanDecisionResponse
)


class LoanApprovalWorkflow:
    """LangGraph-based orchestration for loan approval workflow"""

    def __init__(self):
        self.applicant_agent = create_applicant_agent()
        self.financial_risk_agent = create_financial_risk_agent()
        self.loan_decision_agent = create_loan_decision_agent()
        self.compliance_agent = create_compliance_agent()
        self.graph = self._build_graph()

    def _build_graph(self):
        """Build LangGraph StateGraph for workflow orchestration"""
        workflow = StateGraph(WorkflowState)

        # Add nodes for each agent
        workflow.add_node("initialize", self._initialize_state)
        workflow.add_node(
            "analyze_profile",
            self._analyze_applicant_profile
        )
        workflow.add_node(
            "analyze_financial",
            self._analyze_financial_risk
        )
        workflow.add_node(
            "synthesize_decision",
            self._synthesize_decision
        )
        workflow.add_node(
            "execute_compliance",
            self._execute_compliance
        )
        workflow.add_node("finalize", self._finalize_state)

        # Build workflow edges with parallel execution
        workflow.add_edge("initialize", "analyze_profile")
        workflow.add_edge("initialize", "analyze_financial")

        # Barrier: wait for parallel steps to complete
        workflow.add_edge("analyze_profile", "synthesize_decision")
        workflow.add_edge("analyze_financial", "synthesize_decision")

        # Sequential steps
        workflow.add_edge("synthesize_decision", "execute_compliance")
        workflow.add_edge("execute_compliance", "finalize")
        workflow.add_edge("finalize", END)

        # Set entry point
        workflow.set_entry_point("initialize")

        return workflow.compile()

    def _initialize_state(self, state: WorkflowState) -> WorkflowState:
        """Initialize workflow state"""
        state["case_id"] = generate_case_id(
            state["application"].applicant_id
        )
        state["current_step"] = "initialized"
        state["errors"] = []
        state["processing_complete"] = False
        return state

    def _analyze_applicant_profile(
        self, state: WorkflowState
    ) -> dict:
        """Execute applicant profile analysis agent (parallel node)"""
        try:
            application = state["application"]
            result = run(
                self.applicant_agent.analyze(application)
            )

            return {
                "applicant_profile_result": result
            }
        except Exception as e:
            return {
                "errors": [f"Profile analysis error: {str(e)}"]
            }

    def _analyze_financial_risk(
        self, state: WorkflowState
    ) -> dict:
        """Execute financial risk analysis agent (parallel node)"""
        try:
            application = state["application"]
            result = run(
                self.financial_risk_agent.analyze(application)
            )

            return {
                "financial_risk_result": result
            }
        except Exception as e:
            return {
                "errors": [f"Financial risk analysis error: {str(e)}"]
            }

    def _synthesize_decision(
        self, state: WorkflowState
    ) -> WorkflowState:
        """Execute loan decision synthesis agent"""
        try:
            state["current_step"] = "synthesizing_decision"

            if (
                not state.get("applicant_profile_result")
                or not state.get("financial_risk_result")
            ):
                raise ValueError(
                    "Missing required analysis results"
                )

            application = state["application"]
            result = run(
                self.loan_decision_agent.decide(
                    application,
                    state["applicant_profile_result"],
                    state["financial_risk_result"],
                )
            )

            state["loan_decision_result"] = result
            return state
        except Exception as e:
            state["errors"].append(
                f"Decision synthesis error: {str(e)}"
            )
            return state

    def _execute_compliance(
        self, state: WorkflowState
    ) -> WorkflowState:
        """Execute compliance and action orchestrator agent"""
        try:
            state["current_step"] = "executing_compliance"

            if not state.get("loan_decision_result"):
                raise ValueError("Missing decision result")

            application = state["application"]
            result = run(
                self.compliance_agent.execute(
                    application,
                    state["loan_decision_result"],
                    state["applicant_profile_result"],
                    state["financial_risk_result"],
                )
            )

            state["compliance_result"] = result
            return state
        except Exception as e:
            state["errors"].append(
                f"Compliance execution error: {str(e)}"
            )
            return state

    def _finalize_state(
        self, state: WorkflowState
    ) -> WorkflowState:
        """Finalize workflow state"""
        state["current_step"] = "completed"
        state["processing_complete"] = True
        return state

    async def process_application(
        self, application: LoanApplication
    ) -> LoanDecisionResponse:
        """Execute full loan approval workflow using LangGraph"""

        initial_state: WorkflowState = {
            "application": application,
            "case_id": "",
            "applicant_profile_result": None,
            "financial_risk_result": None,
            "loan_decision_result": None,
            "compliance_result": None,
            "current_step": "start",
            "errors": [],
            "processing_complete": False,
        }

        # Execute graph
        final_state = self.graph.invoke(initial_state)

        # Convert to response
        return self._build_response_from_graph_state(final_state)

    def _build_response_from_graph_state(
        self, state: WorkflowState
    ) -> LoanDecisionResponse:
        """Build final response from LangGraph state"""
        from microservices.schemas import (
            ApplicantProfileResult, FinancialRiskResult, ComplianceResult
        )

        # Ensure all required results exist
        if not state.get("applicant_profile_result"):
            return LoanDecisionResponse(
                case_id=state["case_id"],
                applicant_id=state["application"].applicant_id,
                decision="Requires Manual Review",
                risk_score=0.5,
                confidence=0.0,
                factors=state.get("errors", ["Incomplete analysis"]),
                explanation="Workflow did not complete successfully",
                profile_analysis=ApplicantProfileResult(
                    applicant_id=state["application"].applicant_id,
                    income_stability_score=0.0,
                    employment_risk="Unknown",
                    credit_history_summary={},
                    completeness_flags=state.get("errors", [])
                ),
                financial_analysis=FinancialRiskResult(
                    applicant_id=state["application"].applicant_id,
                    dti_ratio=0.0,
                    credit_risk_level="Unknown",
                    loan_amount_risk="Unknown",
                    anomalies=[],
                    reasoning="Analysis incomplete"
                ),
                compliance_status=ComplianceResult(
                    applicant_id=state["application"].applicant_id,
                    action_taken="Pending",
                    notification_sent=False,
                    case_id=state["case_id"],
                    timestamp=datetime.now().isoformat(),
                    summary="Analysis incomplete"
                ),
                timestamp=datetime.now().isoformat(),
            )

        decision = state["loan_decision_result"]
        compliance = state.get("compliance_result") or ComplianceResult(
            applicant_id=state["application"].applicant_id,
            action_taken="Pending",
            notification_sent=False,
            case_id=state["case_id"],
            timestamp=datetime.now().isoformat(),
            summary="Compliance check pending"
        )

        return LoanDecisionResponse(
            case_id=state["case_id"],
            applicant_id=state["application"].applicant_id,
            decision=decision.decision,
            risk_score=decision.risk_score,
            confidence=decision.confidence_level,
            factors=decision.key_factors,
            explanation=decision.explanation,
            profile_analysis=state["applicant_profile_result"],
            financial_analysis=state["financial_risk_result"],
            compliance_status=compliance,
            timestamp=datetime.now().isoformat(),
        )


def create_workflow():
    """Factory function to create LangGraph-based workflow"""
    return LoanApprovalWorkflow()
