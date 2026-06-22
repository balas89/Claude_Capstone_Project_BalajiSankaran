"""Interactive Test Script - Manual Application Data Entry"""
import requests
import json
from datetime import datetime

API_BASE_URL = "http://localhost:8000"

def get_user_input():
    """Get loan application data from user"""
    print("\n" + "="*70)
    print("LOAN APPLICATION - MANUAL DATA ENTRY")
    print("="*70)
    print("\nPlease enter the following information:\n")

    # Required fields
    applicant_id = input("Applicant ID (e.g., APP_USER_001): ").strip() or "APP_USER_001"
    name = input("Full Name (e.g., John Doe): ").strip() or "John Doe"
    email = input("Email Address (e.g., john@example.com): ").strip() or "john@example.com"

    # Age field
    while True:
        try:
            age = int(input("Age (e.g., 35): ").strip())
            if 18 <= age <= 100:
                break
            else:
                print("  ❌ Age must be between 18 and 100")
        except ValueError:
            print("  ❌ Please enter a valid number")

    # Financial information
    while True:
        try:
            income = float(input("Annual Income in $ (e.g., 120000): ").strip())
            if income > 0:
                break
            else:
                print("  ❌ Income must be greater than 0")
        except ValueError:
            print("  ❌ Please enter a valid number")

    while True:
        try:
            credit_score = int(input("Credit Score (300-850, e.g., 750): ").strip())
            if 300 <= credit_score <= 850:
                break
            else:
                print("  ❌ Credit score must be between 300 and 850")
        except ValueError:
            print("  ❌ Please enter a valid number")

    while True:
        try:
            employment_years = int(input("Years of Employment (e.g., 5): ").strip())
            if employment_years >= 0:
                break
            else:
                print("  ❌ Years must be 0 or more")
        except ValueError:
            print("  ❌ Please enter a valid number")

    print("\nEmployment Type:")
    print("  1. Full-time")
    print("  2. Part-time")
    print("  3. Self-employed")
    print("  4. Salaried")
    emp_choice = input("Select (1-4, default 1 - Full-time): ").strip() or "1"
    employment_types = {
        "1": "Full-time",
        "2": "Part-time",
        "3": "Self-employed",
        "4": "Salaried"
    }
    employment_type = employment_types.get(emp_choice, "Full-time")

    print("\nCredit History:")
    print("  1. Excellent")
    print("  2. Very Good")
    print("  3. Good")
    print("  4. Fair")
    print("  5. Poor")
    credit_choice = input("Select (1-5, default 1 - Excellent): ").strip() or "1"
    credit_histories = {
        "1": "Excellent",
        "2": "Very Good",
        "3": "Good",
        "4": "Fair",
        "5": "Poor"
    }
    credit_history = credit_histories.get(credit_choice, "Excellent")

    # Loan information
    while True:
        try:
            loan_amount = float(input("Requested Loan Amount in $ (e.g., 250000): ").strip())
            if loan_amount > 0:
                break
            else:
                print("  ❌ Loan amount must be greater than 0")
        except ValueError:
            print("  ❌ Please enter a valid number")

    while True:
        try:
            tenure_months = int(input("Loan Tenure in Months (e.g., 60): ").strip())
            if tenure_months > 0:
                break
            else:
                print("  ❌ Tenure must be greater than 0")
        except ValueError:
            print("  ❌ Please enter a valid number")

    while True:
        try:
            existing_liabilities = float(input("Existing Monthly Liabilities in $ (e.g., 2000, default 0): ").strip() or "0")
            if existing_liabilities >= 0:
                break
            else:
                print("  ❌ Liabilities cannot be negative")
        except ValueError:
            print("  ❌ Please enter a valid number")

    # Location
    location = input("Location/State (e.g., New York): ").strip() or "New York"

    # Build application data
    application_data = {
        "applicant_id": applicant_id,
        "name": name,
        "email": email,
        "age": age,
        "income": income,
        "employment_type": employment_type,
        "credit_score": credit_score,
        "employment_years": employment_years,
        "credit_history": credit_history,
        "loan_amount": loan_amount,
        "tenure_months": tenure_months,
        "existing_liabilities": existing_liabilities,
        "location": location,
    }

    return application_data


def display_application_summary(data):
    """Display entered application data for review"""
    print("\n" + "="*70)
    print("APPLICATION SUMMARY")
    print("="*70)
    print("\nAPPLICANT INFORMATION:")
    print(f"  ID: {data['applicant_id']}")
    print(f"  Name: {data['name']}")
    print(f"  Email: {data['email']}")
    print(f"  Age: {data['age']} years old")
    print(f"  Location: {data['location']}")

    print("\nFINANCIAL INFORMATION:")
    print(f"  Annual Income: ${data['income']:,.2f}")
    print(f"  Credit Score: {data['credit_score']}")
    print(f"  Credit History: {data['credit_history']}")
    print(f"  Employment Type: {data['employment_type']}")
    print(f"  Years Employed: {data['employment_years']}")
    print(f"  Monthly Liabilities: ${data['existing_liabilities']:,.2f}")

    print("\nLOAN REQUEST:")
    print(f"  Loan Amount: ${data['loan_amount']:,.2f}")
    print(f"  Tenure: {data['tenure_months']} months")

    # Calculate DTI
    monthly_income = data['income'] / 12
    monthly_payment = (data['loan_amount'] * 0.006) / (1 - (1 + 0.006) ** -data['tenure_months'])
    total_monthly_debt = data['existing_liabilities'] + monthly_payment
    dti = total_monthly_debt / monthly_income if monthly_income > 0 else 1.0

    print(f"\nCALCULATED METRICS:")
    print(f"  Monthly Income: ${monthly_income:,.2f}")
    print(f"  Monthly Loan Payment: ${monthly_payment:,.2f}")
    print(f"  Total Monthly Debt: ${total_monthly_debt:,.2f}")
    print(f"  Debt-to-Income Ratio: {dti:.2%}")

    print("\n" + "="*70)


def test_health():
    """Test health check endpoint"""
    print("\n" + "="*70)
    print("CHECKING SERVICE HEALTH")
    print("="*70)
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ API Service is healthy")
            return True
        else:
            print(f"❌ Service health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API")
        print("   Make sure to start services first: bash run_all.sh")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def submit_application(data):
    """Submit application to API"""
    print("\n" + "="*70)
    print("SUBMITTING APPLICATION")
    print("="*70)

    try:
        response = requests.post(
            f"{API_BASE_URL}/apply-loan",
            json=data,
            timeout=60
        )

        if response.status_code == 200:
            result = response.json()
            print("\n✅ APPLICATION PROCESSED SUCCESSFULLY!\n")

            print("DECISION RESULT:")
            print(f"  Decision: {result['decision']}")
            print(f"  Risk Score: {result['risk_score']:.0%}")
            print(f"  Confidence: {result['confidence']:.0%}")
            print(f"  Case ID: {result['case_id']}")

            print("\nDECISION BASIS:")
            if 'decision_basis' in result:
                print(f"  {result['decision_basis']}")

            print("\nKEY FACTORS:")
            if result['factors']:
                for i, factor in enumerate(result['factors'], 1):
                    print(f"  {i}. {factor}")
            else:
                print("  No specific factors")

            print("\nEXPLANATION:")
            print(f"  {result['explanation']}")

            # Profile Analysis
            if result.get('profile_analysis'):
                profile = result['profile_analysis']
                print("\nAPPLICANT PROFILE ANALYSIS:")
                print(f"  Income Stability Score: {profile.get('income_stability_score', 'N/A')}")
                print(f"  Employment Risk: {profile.get('employment_risk', 'N/A')}")
                if profile.get('credit_history_summary'):
                    credit = profile['credit_history_summary']
                    print(f"  Credit Score: {credit.get('credit_score', 'N/A')}")
                    print(f"  Active Accounts: {credit.get('accounts', 'N/A')}")
                    print(f"  Collections: {credit.get('collections', 'N/A')}")

            # Financial Analysis
            if result.get('financial_analysis'):
                financial = result['financial_analysis']
                print("\nFINANCIAL RISK ANALYSIS:")
                print(f"  DTI Ratio: {financial.get('dti_ratio', 'N/A'):.2%}")
                print(f"  Credit Risk Level: {financial.get('credit_risk_level', 'N/A')}")
                print(f"  Loan Amount Risk: {financial.get('loan_amount_risk', 'N/A')}")
                if financial.get('anomalies'):
                    print(f"  Anomalies Detected: {len(financial['anomalies'])}")
                    for anomaly in financial['anomalies']:
                        print(f"    • {anomaly}")

            print("\n" + "="*70)
            print(f"Processed at: {result['timestamp']}")
            print("="*70)

            return True
        else:
            print(f"❌ Request failed: {response.status_code}")
            print(f"Error: {response.text}")
            return False

    except requests.exceptions.Timeout:
        print("❌ Request timed out (60 seconds)")
        print("   The application processing took too long")
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API")
        print("   Make sure services are running: bash run_all.sh")
    except Exception as e:
        print(f"❌ Error: {e}")

    return False


def main():
    """Main interactive testing flow"""
    print("\n" + "█"*70)
    print("█" + " "*68 + "█")
    print("█" + "  LOAN APPROVAL SYSTEM - INTERACTIVE TEST".center(68) + "█")
    print("█" + " "*68 + "█")
    print("█"*70)

    # Check service health
    if not test_health():
        print("\n⚠️  SERVICES NOT RUNNING")
        print("\nTo use this interactive test, start all services first:")
        print("  bash run_all.sh")
        return

    # Get application data from user
    while True:
        application_data = get_user_input()
        display_application_summary(application_data)

        # Confirm before submitting
        confirm = input("\n✓ Submit this application? (yes/no, default yes): ").strip().lower()
        if confirm in ['', 'yes', 'y']:
            break
        elif confirm in ['no', 'n']:
            print("\n↻ Re-entering application data...\n")
            continue
        else:
            print("  ❌ Invalid input. Please enter 'yes' or 'no'")

    # Submit application
    success = submit_application(application_data)

    # Prompt to continue
    print("\n")
    another = input("Test another application? (yes/no, default no): ").strip().lower()
    if another in ['yes', 'y']:
        main()
    else:
        print("\n✅ Test completed!")
        print("="*70)


if __name__ == "__main__":
    main()
