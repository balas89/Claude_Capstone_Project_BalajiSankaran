"""True MCP Server: Applicant Profile Database using FastMCP"""
import asyncio
from mcp.server.models import InitializationOptions
from mcp.server import Server
from pydantic import BaseModel
from utils.mock_data import MockCreditHistoryDB, MockEmploymentDB


class GetProfileRequest(BaseModel):
    """Request model for applicant profile analysis"""
    applicant_id: str
    age: int
    income: float
    employment_type: str
    credit_score: int


# Create MCP Server
server = Server("applicant-db-mcp")


@server.list_resources()
async def list_resources():
    """List available resources"""
    return [
        {
            "uri": "applicant-db://resources/profile",
            "name": "Applicant Profile Analysis",
            "description": "Analyze applicant profile and return assessment",
            "mimeType": "application/json"
        }
    ]


@server.read_resource()
async def read_resource(uri: str):
    """Read a specific resource"""
    if uri == "applicant-db://resources/profile":
        return "Applicant Profile Analysis Service"
    raise ValueError(f"Unknown resource: {uri}")


@server.list_tools()
async def list_tools():
    """List available tools"""
    return [
        {
            "name": "get_applicant_profile",
            "description": "Analyze applicant profile and return comprehensive assessment including income stability, employment risk, and credit history",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "applicant_id": {
                        "type": "string",
                        "description": "Unique applicant identifier"
                    },
                    "age": {
                        "type": "integer",
                        "description": "Applicant age"
                    },
                    "income": {
                        "type": "number",
                        "description": "Annual income in dollars"
                    },
                    "employment_type": {
                        "type": "string",
                        "description": "Type of employment (Full-time, Part-time, Self-employed, etc.)"
                    },
                    "credit_score": {
                        "type": "integer",
                        "description": "Applicant credit score (300-850)"
                    }
                },
                "required": ["applicant_id", "age", "income", "employment_type", "credit_score"]
            }
        }
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict):
    """Execute a tool"""
    if name != "get_applicant_profile":
        raise ValueError(f"Unknown tool: {name}")

    # Parse request
    request = GetProfileRequest(**arguments)

    # Get credit history
    credit_history = MockCreditHistoryDB.get_credit_history(request.applicant_id)
    employment_info = MockEmploymentDB.verify_employment(
        request.applicant_id, request.employment_type
    )

    # Calculate income stability score (0-1)
    income_stability = 0.0
    if employment_info["verified"]:
        years_employed = employment_info["years_employed"]
        income_stability = min(1.0, years_employed / 10.0 + 0.2)
    else:
        income_stability = 0.2

    # Determine employment risk
    if not employment_info["verified"]:
        employment_risk = "High"
    elif employment_info["job_stability_score"] < 0.5:
        employment_risk = "Medium"
    else:
        employment_risk = "Low"

    # Completeness flags
    completeness_flags = []
    if request.income < 20000:
        completeness_flags.append("Income below minimum threshold")
    if request.age < 21:
        completeness_flags.append("Applicant under 21")
    if credit_history["collections"] > 0:
        completeness_flags.append("Has collections on credit report")
    if credit_history["bankruptcies"] > 0:
        completeness_flags.append("Has bankruptcy history")

    # Credit history summary
    credit_summary = {
        "score": request.credit_score,
        "accounts": credit_history["accounts"],
        "inquiries": credit_history["inquiries"],
        "collections": credit_history["collections"],
        "bankruptcies": credit_history["bankruptcies"],
        "delinquencies": credit_history["delinquencies"],
    }

    return {
        "applicant_id": request.applicant_id,
        "income_stability_score": income_stability,
        "employment_risk": employment_risk,
        "credit_history": credit_summary,
        "completeness_flags": completeness_flags,
        "is_complete": len(completeness_flags) == 0
    }


async def main():
    """Main entry point for MCP server"""
    async with server:
        await server.wait_for_shutdown()


if __name__ == "__main__":
    asyncio.run(main())
