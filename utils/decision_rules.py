"""
Business Logic-Based Decision Rules for Loan Approval
This module implements the actual decision criteria, independent of confidence level
"""

from typing import Dict, Tuple


class LoanDecisionRules:
    """Business rules for loan approval decisions"""

    # DTI Thresholds
    DTI_EXCELLENT = 0.30  # < 30% is excellent
    DTI_GOOD = 0.43       # < 43% is acceptable (recommended)
    DTI_ACCEPTABLE = 0.50 # < 50% is critical threshold
    DTI_REJECT = 0.50     # >= 50% triggers rejection

    # Credit Score Thresholds
    CREDIT_EXCELLENT = 750
    CREDIT_VERY_GOOD = 700
    CREDIT_GOOD = 650
    CREDIT_FAIR = 600
    CREDIT_POOR = 600

    # Loan-to-Income Ratio
    LTI_EXCELLENT = 2.0
    LTI_GOOD = 2.5
    LTI_ACCEPTABLE = 3.0
    LTI_HIGH_RISK = 4.0

    # Income Stability
    INCOME_STABILITY_EXCELLENT = 0.8
    INCOME_STABILITY_GOOD = 0.6
    INCOME_STABILITY_FAIR = 0.4
    INCOME_STABILITY_POOR = 0.2

    @staticmethod
    def make_decision(
        dti_ratio: float,
        credit_score: int,
        loan_to_income: float,
        income_stability: float,
        employment_risk: str,
        anomalies: list,
        completeness_flags: list
    ) -> Tuple[str, float, str]:
        """
        Make a loan decision based on business rules, NOT confidence level.

        Returns:
            Tuple of (decision, risk_score, reasoning)
            - decision: "Approve", "Reject", or "Requires Manual Review"
            - risk_score: 0.0 (lowest risk) to 1.0 (highest risk)
            - reasoning: Human-readable explanation
        """

        reasons = []
        risk_factors = 0
        total_factors = 0

        # ========== HARD REJECTION CRITERIA ==========
        # These alone can cause rejection

        # 1. DTI too high
        if dti_ratio >= LoanDecisionRules.DTI_REJECT:
            return ("Reject", 0.95, f"DTI ratio {dti_ratio:.2f} exceeds maximum threshold of 0.50")

        # 2. Credit score too low
        if credit_score < LoanDecisionRules.CREDIT_FAIR:
            return ("Reject", 0.90, f"Credit score {credit_score} below minimum threshold of 600")

        # 3. Too many severe anomalies
        severe_anomalies = [a for a in anomalies if any(
            keyword in a.lower() for keyword in ["bankruptcy", "foreclosure", "collection"]
        )]
        if len(severe_anomalies) >= 2:
            return ("Reject", 0.85, f"Multiple severe credit events detected: {', '.join(severe_anomalies)}")

        # 4. Completeness flags that indicate ineligibility
        ineligibility_flags = [f for f in completeness_flags if any(
            keyword in f.lower() for keyword in ["under 21", "invalid", "fraud"]
        )]
        if ineligibility_flags:
            return ("Reject", 0.85, f"Application fails eligibility: {', '.join(ineligibility_flags)}")

        # ========== APPROVAL CRITERIA ==========
        # All must be positive

        approval_score = 100.0  # Start with perfect score

        # Credit Score Evaluation (Weight: 25%)
        if credit_score >= LoanDecisionRules.CREDIT_EXCELLENT:
            reasons.append(f"✓ Excellent credit score: {credit_score}")
        elif credit_score >= LoanDecisionRules.CREDIT_VERY_GOOD:
            reasons.append(f"✓ Very good credit score: {credit_score}")
            approval_score -= 5
        elif credit_score >= LoanDecisionRules.CREDIT_GOOD:
            reasons.append(f"⚠ Fair credit score: {credit_score}")
            approval_score -= 15
        else:
            approval_score -= 25

        # DTI Ratio Evaluation (Weight: 25%)
        if dti_ratio < LoanDecisionRules.DTI_EXCELLENT:
            reasons.append(f"✓ Excellent DTI ratio: {dti_ratio:.2f}")
        elif dti_ratio < LoanDecisionRules.DTI_GOOD:
            reasons.append(f"✓ Good DTI ratio: {dti_ratio:.2f}")
            approval_score -= 5
        elif dti_ratio < LoanDecisionRules.DTI_ACCEPTABLE:
            reasons.append(f"⚠ Acceptable DTI ratio: {dti_ratio:.2f} (near threshold)")
            approval_score -= 15
        else:
            approval_score -= 30

        # Loan-to-Income Ratio (Weight: 20%)
        if loan_to_income < LoanDecisionRules.LTI_EXCELLENT:
            reasons.append(f"✓ Low loan-to-income ratio: {loan_to_income:.2f}x")
        elif loan_to_income < LoanDecisionRules.LTI_GOOD:
            reasons.append(f"✓ Reasonable loan-to-income ratio: {loan_to_income:.2f}x")
            approval_score -= 5
        elif loan_to_income < LoanDecisionRules.LTI_ACCEPTABLE:
            reasons.append(f"⚠ High loan-to-income ratio: {loan_to_income:.2f}x")
            approval_score -= 15
        else:
            approval_score -= 25

        # Income Stability (Weight: 15%)
        if income_stability >= LoanDecisionRules.INCOME_STABILITY_EXCELLENT:
            reasons.append(f"✓ High income stability: {income_stability:.2f}")
        elif income_stability >= LoanDecisionRules.INCOME_STABILITY_GOOD:
            reasons.append(f"✓ Good income stability: {income_stability:.2f}")
            approval_score -= 5
        elif income_stability >= LoanDecisionRules.INCOME_STABILITY_FAIR:
            reasons.append(f"⚠ Fair income stability: {income_stability:.2f}")
            approval_score -= 15
        else:
            approval_score -= 20

        # Employment Risk (Weight: 10%)
        if employment_risk == "Low":
            reasons.append("✓ Low employment risk")
        elif employment_risk == "Medium":
            reasons.append("⚠ Medium employment risk")
            approval_score -= 10
        else:  # High
            reasons.append("✗ High employment risk")
            approval_score -= 20

        # Anomalies (Weight: 5%)
        if len(anomalies) == 0:
            reasons.append("✓ No anomalies detected")
        elif len(anomalies) == 1:
            reasons.append(f"⚠ 1 anomaly detected: {anomalies[0]}")
            approval_score -= 10
        else:
            reasons.append(f"✗ Multiple anomalies detected ({len(anomalies)})")
            approval_score -= 15

        # ========== DECISION LOGIC ==========
        # Calculate final decision based on approval score

        risk_score = max(0.0, min(1.0, (100.0 - approval_score) / 100.0))

        if approval_score >= 85:
            decision = "Approve"
            reasoning = "Applicant meets all approval criteria with strong financial metrics"
        elif approval_score >= 70:
            decision = "Approve"
            reasoning = "Applicant meets approval criteria. Some factors are near thresholds but acceptable"
        elif approval_score >= 50:
            decision = "Requires Manual Review"
            reasoning = "Mixed financial profile. Recommend manual underwriter review before final decision"
        else:
            decision = "Requires Manual Review"
            reasoning = "Significant risk factors present. Manual review required to determine eligibility"

        # Add reason summary
        full_reasoning = f"{reasoning}\n\nFactors:\n" + "\n".join(reasons)

        return (decision, risk_score, full_reasoning)

    @staticmethod
    def calculate_risk_score(
        dti_ratio: float,
        credit_score: int,
        loan_to_income: float,
        income_stability: float,
        employment_risk: str,
        anomaly_count: int
    ) -> float:
        """
        Calculate a normalized risk score (0.0 = lowest risk, 1.0 = highest risk)
        """
        risk_components = []

        # DTI Component (0-0.3)
        if dti_ratio <= 0.30:
            risk_components.append(0.05)
        elif dti_ratio <= 0.43:
            risk_components.append(0.10)
        elif dti_ratio <= 0.50:
            risk_components.append(0.20)
        else:
            risk_components.append(0.30)

        # Credit Score Component (0-0.25)
        if credit_score >= 750:
            risk_components.append(0.05)
        elif credit_score >= 700:
            risk_components.append(0.10)
        elif credit_score >= 650:
            risk_components.append(0.15)
        elif credit_score >= 600:
            risk_components.append(0.20)
        else:
            risk_components.append(0.25)

        # LTI Component (0-0.2)
        if loan_to_income <= 2.0:
            risk_components.append(0.05)
        elif loan_to_income <= 2.5:
            risk_components.append(0.08)
        elif loan_to_income <= 3.0:
            risk_components.append(0.12)
        elif loan_to_income <= 4.0:
            risk_components.append(0.17)
        else:
            risk_components.append(0.20)

        # Income Stability Component (0-0.15)
        if income_stability >= 0.8:
            risk_components.append(0.03)
        elif income_stability >= 0.6:
            risk_components.append(0.06)
        elif income_stability >= 0.4:
            risk_components.append(0.10)
        else:
            risk_components.append(0.15)

        # Employment Risk Component (0-0.1)
        if employment_risk == "Low":
            risk_components.append(0.02)
        elif employment_risk == "Medium":
            risk_components.append(0.06)
        else:
            risk_components.append(0.10)

        # Anomalies Component (0-0.1)
        anomaly_risk = min(0.10, anomaly_count * 0.03)
        risk_components.append(anomaly_risk)

        # Calculate weighted average
        total_risk = sum(risk_components)
        return min(1.0, total_risk)
