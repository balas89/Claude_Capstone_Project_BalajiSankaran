"""FastAPI routes for loan application processing"""
from fastapi import APIRouter, HTTPException
from datetime import datetime
from microservices.schemas import LoanApplication, LoanDecisionResponse, HealthCheck
from orchestration.workflow import create_workflow
import asyncio

router = APIRouter()
workflow = create_workflow()

@router.post("/apply-loan", response_model=LoanDecisionResponse)
async def apply_for_loan(application: LoanApplication) -> LoanDecisionResponse:
    """Process loan application through multi-agent workflow"""
    try:
        result = await workflow.process_application(application)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Loan application processing failed: {str(e)}")

@router.get("/health", response_model=HealthCheck)
async def health_check() -> HealthCheck:
    """Health check endpoint"""
    return HealthCheck(
        status="healthy",
        timestamp=datetime.now().isoformat()
    )
