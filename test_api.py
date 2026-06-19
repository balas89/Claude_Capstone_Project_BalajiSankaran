"""Test script for the Loan Approval System API"""
import requests
import json
from datetime import datetime

API_BASE_URL = "http://localhost:8000"

# Test cases
TEST_CASES = {
    "approval_case": {
        "applicant_id": "TEST_APPROVAL_001",
        "age": 35,
        "income": 120000,
        "employment_type": "Salaried",
        "credit_score": 780,
        "loan_amount": 100000,
        "tenure_months": 60,
        "existing_liabilities": 10000,
        "location": "New York",
    },
    "rejection_case": {
        "applicant_id": "TEST_REJECTION_001",
        "age": 25,
        "income": 25000,
        "employment_type": "Self-Employed",
        "credit_score": 550,
        "loan_amount": 300000,
        "tenure_months": 120,
        "existing_liabilities": 80000,
        "location": "California",
    },
    "review_case": {
        "applicant_id": "TEST_REVIEW_001",
        "age": 45,
        "income": 75000,
        "employment_type": "Salaried",
        "credit_score": 680,
        "loan_amount": 150000,
        "tenure_months": 84,
        "existing_liabilities": 35000,
        "location": "Texas",
    },
}

def test_health():
    """Test health check endpoint"""
    print("\n" + "="*60)
    print("Testing Health Check Endpoint")
    print("="*60)
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health check passed")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_loan_application(name, application_data):
    """Test loan application endpoint"""
    print("\n" + "="*60)
    print(f"Testing Loan Application: {name}")
    print("="*60)
    print(f"Input: {json.dumps(application_data, indent=2)}")

    try:
        response = requests.post(
            f"{API_BASE_URL}/apply-loan",
            json=application_data,
            timeout=60
        )

        if response.status_code == 200:
            result = response.json()
            print(f"\n✅ Application processed successfully")
            print(f"Decision: {result['decision']}")
            print(f"Risk Score: {result['risk_score']:.2%}")
            print(f"Confidence: {result['confidence']:.2%}")
            print(f"Case ID: {result['case_id']}")
            print(f"Explanation: {result['explanation']}")
            print(f"\nKey Factors:")
            for factor in result['factors']:
                print(f"  • {factor}")

            return result
        else:
            print(f"❌ Request failed: {response.status_code}")
            print(response.text)
            return None
    except requests.exceptions.Timeout:
        print("❌ Request timed out")
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Ensure microservice is running on port 8000")
    except Exception as e:
        print(f"❌ Error: {e}")
    return None

def run_all_tests():
    """Run all test cases"""
    print("\n" + "█"*60)
    print("  LOAN APPROVAL SYSTEM - API TEST SUITE")
    print("█"*60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Test health
    test_health()

    # Test applications
    results = {}
    for test_name, test_data in TEST_CASES.items():
        result = test_loan_application(test_name, test_data)
        if result:
            results[test_name] = result

    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    for test_name, result in results.items():
        status = "✅" if result else "❌"
        decision = result.get('decision', 'Unknown') if result else 'Failed'
        print(f"{status} {test_name}: {decision}")

    print(f"\nCompleted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    run_all_tests()
