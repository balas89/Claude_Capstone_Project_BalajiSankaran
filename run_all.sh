#!/bin/bash

# Multi-Agent Loan Approval System - All Services Startup Script
# Run with: bash run_all.sh

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║   Starting Multi-Agent Loan Approval System                   ║"
echo "║   All 6 Services                                              ║"
echo "╚════════════════════════════════════════════════════════════════╝"

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo ""
echo -e "${YELLOW}Starting all services...${NC}"
echo ""

# Start all services in background
echo -e "${GREEN}[1/6]${NC} Starting Applicant DB MCP (Port 8001)..."
python -m uvicorn mcp_servers.applicant_db:app --host 0.0.0.0 --port 8001 --reload > logs/applicant_db.log 2>&1 &
APP_DB_PID=$!

echo -e "${GREEN}[2/6]${NC} Starting Risk Rules DB MCP (Port 8002)..."
python -m uvicorn mcp_servers.risk_rules_db:app --host 0.0.0.0 --port 8002 --reload > logs/risk_rules_db.log 2>&1 &
RISK_DB_PID=$!

echo -e "${GREEN}[3/6]${NC} Starting Decision Synthesis MCP (Port 8003)..."
python -m uvicorn mcp_servers.decision_synthesis:app --host 0.0.0.0 --port 8003 --reload > logs/decision_synthesis.log 2>&1 &
DECISION_PID=$!

echo -e "${GREEN}[4/6]${NC} Starting Notification System MCP (Port 8004)..."
python -m uvicorn mcp_servers.notification_system:app --host 0.0.0.0 --port 8004 --reload > logs/notification_system.log 2>&1 &
NOTIFICATION_PID=$!

echo -e "${GREEN}[5/6]${NC} Starting FastAPI Microservice (Port 8000)..."
python -m uvicorn microservices.app:app --host 0.0.0.0 --port 8000 --reload > logs/fastapi.log 2>&1 &
FASTAPI_PID=$!

echo -e "${GREEN}[6/6]${NC} Starting Streamlit UI (Port 8501)..."
streamlit run ui/streamlit_app.py --server.port 8501 --logger.level=debug > logs/streamlit.log 2>&1 &
STREAMLIT_PID=$!

# Store PIDs for cleanup
echo "$APP_DB_PID" > .pids
echo "$RISK_DB_PID" >> .pids
echo "$DECISION_PID" >> .pids
echo "$NOTIFICATION_PID" >> .pids
echo "$FASTAPI_PID" >> .pids
echo "$STREAMLIT_PID" >> .pids

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                   ✅ ALL SERVICES STARTED ✅                  ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "Services running:"
echo "  ✓ Applicant DB MCP:        http://localhost:8001"
echo "  ✓ Risk Rules DB MCP:       http://localhost:8002"
echo "  ✓ Decision Synthesis MCP:  http://localhost:8003"
echo "  ✓ Notification System MCP: http://localhost:8004"
echo "  ✓ FastAPI Service:         http://localhost:8000"
echo "  ✓ Streamlit UI:            http://localhost:8501 ← OPEN THIS"
echo ""
echo "API Documentation: http://localhost:8000/docs"
echo ""
echo "To stop all services, run: bash stop_all.sh"
echo ""
echo "Logs available in: logs/ directory"
echo ""
echo "Opening browser..."
sleep 3

# Try to open browser
if command -v xdg-open > /dev/null; then
    xdg-open http://localhost:8501 &
elif command -v open > /dev/null; then
    open http://localhost:8501 &
elif command -v start > /dev/null; then
    start http://localhost:8501 &
fi

echo "Press Ctrl+C to stop all services (or run: bash stop_all.sh)"

# Wait for all processes
wait
