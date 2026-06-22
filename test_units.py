"""Unit tests for core business logic - No HTTP dependencies"""
import sys
sys.path.insert(0, '/home/ubuntu/Desktop/Capstone_project_3')

from utils.decision_rules import LoanDecisionRules

print("╔════════════════════════════════════════════════════════════╗")
print("║  UNIT TESTS - Decision Rules (No HTTP Dependencies)        ║")
print("╚════════════════════════════════════════════════════════════╝\n")

test_count = 0
passed = 0
failed = 0

def test(name, dti, credit, lti, stability, emp_risk, anomalies, completeness, expected_decision):
    global test_count, passed, failed
    test_count += 1
    
    decision, risk_score, reasoning = LoanDecisionRules.make_decision(
        dti_ratio=dti,
        credit_score=credit,
        loan_to_income=lti,
        income_stability=stability,
        employment_risk=emp_risk,
        anomalies=anomalies,
        completeness_flags=completeness
    )
    
    if decision == expected_decision:
        print(f"✅ TEST {test_count}: {name}")
        print(f"   Decision: {decision} | Risk Score: {risk_score:.2f}\n")
        passed += 1
        return True
    else:
        print(f"❌ TEST {test_count}: {name}")
        print(f"   Expected: {expected_decision}")
        print(f"   Got: {decision}\n")
        failed += 1
        return False

print("HARD REJECTION CRITERIA TESTS")
print("="*60)
test("DTI >= 50%", dti=0.55, credit=750, lti=2.5, stability=0.8, 
     emp_risk="Low", anomalies=[], completeness=[], expected_decision="Reject")

test("Credit < 600", dti=0.3, credit=550, lti=2.0, stability=0.8,
     emp_risk="Low", anomalies=[], completeness=[], expected_decision="Reject")

test("Multiple severe anomalies", dti=0.3, credit=750, lti=2.0, stability=0.8,
     emp_risk="Low", anomalies=["Recent bankruptcy", "Foreclosure"], completeness=[],
     expected_decision="Reject")

print("\nAPPROVAL CRITERIA TESTS")
print("="*60)
test("Excellent profile (High approval score)", dti=0.30, credit=780, lti=2.0, stability=0.9,
     emp_risk="Low", anomalies=[], completeness=[], expected_decision="Approve")

test("Good profile (Acceptable DTI < 43%)", dti=0.42, credit=720, lti=2.5, stability=0.8,
     emp_risk="Low", anomalies=[], completeness=[], expected_decision="Approve")

test("Fair credit but acceptable metrics", dti=0.35, credit=680, lti=2.3, stability=0.7,
     emp_risk="Low", anomalies=[], completeness=[], expected_decision="Approve")

print("\nMANUAL REVIEW CRITERIA TESTS")
print("="*60)
test("DTI near threshold", dti=0.48, credit=700, lti=2.8, stability=0.6,
     emp_risk="Medium", anomalies=[], completeness=[], expected_decision="Requires Manual Review")

test("Multiple moderate risk factors", dti=0.45, credit=650, lti=3.2, stability=0.5,
     emp_risk="Medium", anomalies=["One anomaly"], completeness=[], expected_decision="Requires Manual Review")

test("Fair income stability", dti=0.35, credit=720, lti=2.0, stability=0.4,
     emp_risk="Medium", anomalies=[], completeness=[], expected_decision="Requires Manual Review")

print("\nRISK SCORE TESTS")
print("="*60)

def test_risk_score(dti, credit, lti, stability, emp_risk, anomaly_count, expected_max_risk):
    score = LoanDecisionRules.calculate_risk_score(dti, credit, lti, stability, emp_risk, anomaly_count)
    if score <= expected_max_risk:
        print(f"✅ Risk score {score:.2f} <= {expected_max_risk:.2f}")
        return True
    else:
        print(f"❌ Risk score {score:.2f} > {expected_max_risk:.2f}")
        return False

print("Low risk profile:")
test_risk_score(dti=0.30, credit=780, lti=2.0, stability=0.9, emp_risk="Low", anomaly_count=0, expected_max_risk=0.15)

print("\nHigh risk profile:")
test_risk_score(dti=0.48, credit=600, lti=4.0, stability=0.2, emp_risk="High", anomaly_count=2, expected_max_risk=0.90)

print("\n" + "="*60)
print(f"SUMMARY: {passed}/{test_count} tests passed, {failed} failed")
print("="*60)

if failed == 0:
    print("✅ ALL TESTS PASSED!")
    sys.exit(0)
else:
    print(f"❌ {failed} tests failed")
    sys.exit(1)
