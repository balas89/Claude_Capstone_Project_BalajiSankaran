"""MCP Server: Compliance & Notification System"""
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from utils.mock_data import MockAuditTrailDB, MockNotificationService, generate_case_id
from utils.mock_data import MockComplianceRulesDB

app = FastAPI(title="Notification System MCP Server")

class NotificationRequest(BaseModel):
    applicant_id: str
    location: str
    decision: str
    risk_factors: dict
    profile_analysis: dict

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "notification_system"}

@app.post("/execute_compliance_and_notify")
async def execute_compliance_and_notify(request: NotificationRequest):
    """Execute compliance checks and send notifications"""

    # Generate case ID
    case_id = generate_case_id(request.applicant_id)

    # Run compliance check
    compliance_check = MockComplianceRulesDB.check_compliance(
        request.applicant_id, request.location
    )

    if not compliance_check["compliant"]:
        return {
            "applicant_id": request.applicant_id,
            "action_taken": "Application blocked - compliance check failed",
            "notification_sent": False,
            "case_id": case_id,
            "timestamp": datetime.now().isoformat(),
            "summary": f"Compliance check failed for location {request.location}",
        }

    # Log to audit trail
    audit_entry = MockAuditTrailDB.log_decision(
        case_id,
        request.decision,
        {
            "risk_factors": request.risk_factors,
            "compliance_verified": compliance_check["compliant"],
        }
    )

    # Send notification
    notification = MockNotificationService.send_notification(
        case_id,
        request.applicant_id,
        request.decision,
        contact_info="applicant@example.com"
    )

    return {
        "applicant_id": request.applicant_id,
        "action_taken": f"Decision {request.decision} - Notification sent",
        "notification_sent": notification["sent"],
        "case_id": case_id,
        "timestamp": notification["timestamp"],
        "summary": f"Application {case_id} processed with decision: {request.decision}",
    }

@app.get("/audit_trail")
async def get_audit_trail():
    """Retrieve audit trail"""
    return {"audit_trail": MockAuditTrailDB.get_audit_trail()}

@app.get("/notifications")
async def get_notifications():
    """Retrieve sent notifications"""
    return {"notifications": MockNotificationService.notifications_sent}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)
