from datetime import datetime, timedelta
import random

class MockCreditHistoryDB:
    """Mock credit history database"""

    @staticmethod
    def get_credit_history(applicant_id: str) -> dict:
        """Simulate credit history lookup"""
        base_score = 650 + hash(applicant_id) % 200
        return {
            "applicant_id": applicant_id,
            "credit_score": base_score,
            "payment_history": "Good" if base_score > 700 else "Fair" if base_score > 600 else "Poor",
            "accounts_count": random.randint(3, 15),
            "late_payments_6m": random.randint(0, 3),
            "late_payments_12m": random.randint(0, 5),
            "inquiries_6m": random.randint(0, 5),
            "collections": random.randint(0, 2),
        }

class MockEmploymentDB:
    """Mock employment verification database"""

    @staticmethod
    def verify_employment(applicant_id: str, employment_type: str) -> dict:
        """Simulate employment verification"""
        is_valid = hash(applicant_id) % 10 < 9
        return {
            "applicant_id": applicant_id,
            "employment_type": employment_type,
            "verified": is_valid,
            "employment_status": "Employed" if is_valid else "Unemployed",
            "years_employed": random.randint(1, 20) if is_valid else 0,
            "job_stability_score": random.uniform(0.5, 1.0) if is_valid else 0.0,
        }

class MockComplianceRulesDB:
    """Mock compliance rules database"""

    @staticmethod
    def check_compliance(applicant_id: str, location: str) -> dict:
        """Simulate compliance check"""
        return {
            "applicant_id": applicant_id,
            "location": location,
            "compliant": True,
            "regulatory_restrictions": [],
            "age_verified": True,
            "identity_verified": hash(applicant_id) % 10 < 9,
            "sanctions_list_checked": True,
        }

class MockAuditTrailDB:
    """Mock audit trail database"""

    decisions_log = []

    @classmethod
    def log_decision(cls, case_id: str, decision: str, reasoning: dict) -> dict:
        """Log decision to audit trail"""
        entry = {
            "case_id": case_id,
            "timestamp": datetime.now().isoformat(),
            "decision": decision,
            "reasoning": reasoning,
        }
        cls.decisions_log.append(entry)
        return entry

    @classmethod
    def get_audit_trail(cls) -> list:
        """Retrieve audit trail"""
        return cls.decisions_log

class MockNotificationService:
    """Mock notification service"""

    notifications_sent = []

    @classmethod
    def send_notification(cls, case_id: str, applicant_id: str, decision: str,
                         contact_info: str = None) -> dict:
        """Send notification"""
        notification = {
            "case_id": case_id,
            "applicant_id": applicant_id,
            "decision": decision,
            "timestamp": datetime.now().isoformat(),
            "contact_info": contact_info,
            "sent": True,
        }
        cls.notifications_sent.append(notification)
        return notification

def generate_case_id(applicant_id: str) -> str:
    """Generate unique case ID"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"CASE_{applicant_id}_{timestamp}"
