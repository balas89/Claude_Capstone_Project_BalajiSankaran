from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class LoanApplication(BaseModel):
    """Loan application input schema"""
    applicant_id: str
    age: int
    income: float
    employment_type: str
    credit_score: int
    loan_amount: float
    tenure_months: int
    existing_liabilities: float
    location: str

class ApplicantProfileResult(BaseModel):
    """Result from Applicant Profile Agent"""
    applicant_id: str
    income_stability_score: float
    employment_risk: str
    credit_history_summary: dict
    completeness_flags: List[str]

class FinancialRiskResult(BaseModel):
    """Result from Financial Risk Analysis Agent"""
    applicant_id: str
    dti_ratio: float
    credit_risk_level: str
    loan_amount_risk: str
    anomalies: List[str]
    reasoning: str

class LoanDecisionResult(BaseModel):
    """Result from Loan Decision Agent"""
    applicant_id: str
    decision: str  # "Approve", "Reject", or "Requires Manual Review"
    risk_score: float
    confidence_level: float
    key_factors: List[str]
    explanation: str

class ComplianceResult(BaseModel):
    """Result from Compliance Agent"""
    applicant_id: str
    action_taken: str
    notification_sent: bool
    case_id: str
    timestamp: str
    summary: str

class LoanDecisionResponse(BaseModel):
    """Final API response"""
    case_id: str
    applicant_id: str
    decision: str
    risk_score: float
    confidence: float
    factors: List[str]
    explanation: str
    profile_analysis: ApplicantProfileResult
    financial_analysis: FinancialRiskResult
    compliance_status: ComplianceResult
    timestamp: str

class HealthCheck(BaseModel):
    """Health check response"""
    status: str
    timestamp: str
