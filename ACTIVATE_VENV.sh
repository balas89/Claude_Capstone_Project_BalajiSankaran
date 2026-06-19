#!/bin/bash
# Quick activation script for virtual environment

echo "Activating virtual environment..."
source venv/bin/activate

echo "✅ Virtual environment activated!"
echo "Current Python: $(which python3)"
echo ""
echo "You can now run:"
echo "  python3 -m mcp_servers.applicant_db"
echo "  python3 -m mcp_servers.risk_rules_db"
echo "  python3 -m mcp_servers.decision_synthesis"
echo "  python3 -m mcp_servers.notification_system"
echo "  python3 -m microservices.app"
echo "  streamlit run ui/streamlit_app.py"
echo "  python3 test_api.py"
echo ""
echo "Type 'deactivate' to exit the virtual environment"
