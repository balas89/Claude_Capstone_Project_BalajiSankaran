"""True MCP Server: Notification System using FastMCP"""
import asyncio
from datetime import datetime
from mcp.server import Server
from pydantic import BaseModel
from utils.mock_data import MockAuditTrailDB, MockNotificationService


class ExecuteComplianceRequest(BaseModel):
    """Request model for compliance execution"""
    applicant_id: str
    case_id: str
    decision: str
    risk_score: float
    email: str = ""


# Create MCP Server
server = Server("notification-system-mcp")


@server.list_resources()
async def list_resources():
    """List available resources"""
    return [
        {
            "uri": "notification://resources/compliance",
            "name": "Compliance & Notification Engine",
            "description": "Execute compliance checks and send notifications",
            "mimeType": "application/json"
        },
        {
            "uri": "notification://resources/audit",
            "name": "Audit Trail System",
            "description": "Log and track all decisions and actions",
            "mimeType": "application/json"
        }
    ]


@server.read_resource()
async def read_resource(uri: str):
    """Read a specific resource"""
    if uri == "notification://resources/compliance":
        return "Compliance and Notification Engine"
    elif uri == "notification://resources/audit":
        return "Audit Trail and Logging System"
    raise ValueError(f"Unknown resource: {uri}")


@server.list_tools()
async def list_tools():
    """List available tools"""
    return [
        {
            "name": "execute_compliance",
            "description": "Execute compliance checks, log audit trail, and send notifications for loan decision",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "applicant_id": {
                        "type": "string",
                        "description": "Unique applicant identifier"
                    },
                    "case_id": {
                        "type": "string",
                        "description": "Unique case identifier for tracking"
                    },
                    "decision": {
                        "type": "string",
                        "description": "Loan decision (Approve, Reject, Requires Manual Review)",
                        "enum": ["Approve", "Reject", "Requires Manual Review"]
                    },
                    "risk_score": {
                        "type": "number",
                        "description": "Risk score (0.0 to 1.0)"
                    },
                    "email": {
                        "type": "string",
                        "description": "Applicant email for notification",
                        "default": ""
                    }
                },
                "required": ["applicant_id", "case_id", "decision", "risk_score"]
            }
        }
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict):
    """Execute a tool"""
    if name != "execute_compliance":
        raise ValueError(f"Unknown tool: {name}")

    # Parse request
    request = ExecuteComplianceRequest(**arguments)

    # Execute compliance checks
    compliance_status = "Pass"
    compliance_notes = []

    # Check 1: KYC (Know Your Customer) - Simulated
    compliance_notes.append("KYC verification: Passed")

    # Check 2: Sanction screening - Simulated
    compliance_notes.append("Sanction screening: Clear")

    # Check 3: DTI validation - Simulated
    if request.risk_score > 0.7:
        compliance_notes.append("High risk flag: Requires additional review")
    else:
        compliance_notes.append("Risk assessment: Acceptable")

    # Determine action based on decision
    if request.decision == "Approve":
        action_taken = "Application Approved"
        notification_type = "approval"
    elif request.decision == "Reject":
        action_taken = "Application Rejected"
        notification_type = "rejection"
    else:
        action_taken = "Application Flagged for Manual Review"
        notification_type = "review"

    # Log audit trail
    audit_entry = {
        "case_id": request.case_id,
        "applicant_id": request.applicant_id,
        "decision": request.decision,
        "risk_score": request.risk_score,
        "action": action_taken,
        "timestamp": datetime.now().isoformat(),
        "compliance_status": compliance_status,
        "compliance_notes": compliance_notes
    }

    # Store in audit trail
    MockAuditTrailDB.log_decision(audit_entry)

    # Send notification
    notification_sent = False
    notification_channel = None

    if request.email:
        # Send email notification
        notification_result = MockNotificationService.send_email_notification(
            recipient=request.email,
            subject=f"Loan Application Decision: {request.decision}",
            body=f"Your loan application has been {notification_type}. Case ID: {request.case_id}",
            notification_type=notification_type
        )
        notification_sent = notification_result.get("sent", False)
        notification_channel = "email"

    # Send in-app notification (always)
    in_app_notification = MockNotificationService.send_in_app_notification(
        applicant_id=request.applicant_id,
        title=f"Loan Decision: {request.decision}",
        message=f"Your application has been processed. Case ID: {request.case_id}",
        notification_type=notification_type
    )

    return {
        "applicant_id": request.applicant_id,
        "case_id": request.case_id,
        "action_taken": action_taken,
        "notification_sent": notification_sent,
        "notification_channel": notification_channel or "in-app",
        "compliance_status": compliance_status,
        "compliance_notes": compliance_notes,
        "timestamp": datetime.now().isoformat(),
        "audit_logged": True,
        "summary": f"Decision {request.decision} processed and logged. Notification sent via {notification_channel or 'in-app'}."
    }


async def main():
    """Main entry point for MCP server"""
    async with server:
        await server.wait_for_shutdown()


if __name__ == "__main__":
    asyncio.run(main())
