#!/bin/bash
# Start all services for the Loan Approval System

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

echo "🚀 Starting Loan Approval System..."
echo "Project directory: $PROJECT_DIR"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
else
    echo "⚠️ Virtual environment not found. Create with: python -m venv venv"
fi

# Load environment variables
if [ -f ".env" ]; then
    echo "Loading environment variables from .env"
    export $(cat .env | grep -v '#' | xargs)
else
    echo "⚠️ .env file not found. Copy from .env.example: cp .env.example .env"
fi

# Function to start a service
start_service() {
    local name=$1
    local port=$2
    local module=$3

    echo ""
    echo "▶️  Starting $name on port $port..."
    echo "   Command: python -m $module"

    python -m $module &
    SERVICE_PID=$!
    echo "   PID: $SERVICE_PID"
    echo "$SERVICE_PID" >> .pids

    sleep 2

    # Check if service is running
    if ! ps -p $SERVICE_PID > /dev/null; then
        echo "❌ Failed to start $name"
        exit 1
    fi
    echo "✅ $name started"
}

# Initialize PID file
: > .pids

# Start MCP Servers
echo ""
echo "════════════════════════════════════"
echo "  Starting MCP Servers..."
echo "════════════════════════════════════"
start_service "Applicant DB MCP Server" "8001" "mcp_servers.applicant_db"
start_service "Risk Rules DB MCP Server" "8002" "mcp_servers.risk_rules_db"
start_service "Decision Synthesis MCP Server" "8003" "mcp_servers.decision_synthesis"
start_service "Notification System MCP Server" "8004" "mcp_servers.notification_system"

# Wait for MCP servers to be ready
echo ""
echo "Waiting for MCP servers to initialize..."
sleep 3

# Start FastAPI Microservice
echo ""
echo "════════════════════════════════════"
echo "  Starting FastAPI Microservice..."
echo "════════════════════════════════════"
start_service "FastAPI Microservice" "8000" "microservices.app"

# Start Streamlit UI
echo ""
echo "════════════════════════════════════"
echo "  Starting Streamlit UI..."
echo "════════════════════════════════════"

echo ""
echo "▶️  Starting Streamlit UI..."
streamlit run ui/streamlit_app.py &
STREAMLIT_PID=$!
echo "   PID: $STREAMLIT_PID"
echo "$STREAMLIT_PID" >> .pids

# Display running services
echo ""
echo "════════════════════════════════════"
echo "  ✅ All Services Started!"
echo "════════════════════════════════════"
echo ""
echo "📍 Service URLs:"
echo "   Applicant DB MCP:        http://localhost:8001"
echo "   Risk Rules DB MCP:       http://localhost:8002"
echo "   Decision Synthesis MCP:  http://localhost:8003"
echo "   Notification System MCP: http://localhost:8004"
echo "   FastAPI Microservice:    http://localhost:8000"
echo "   Streamlit UI:            http://localhost:8501"
echo ""
echo "📚 API Documentation: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services..."
echo ""

# Cleanup function
cleanup() {
    echo ""
    echo "Shutting down services..."
    if [ -f ".pids" ]; then
        while read pid; do
            if kill -0 $pid 2>/dev/null; then
                echo "Stopping process $pid..."
                kill $pid 2>/dev/null || true
            fi
        done < .pids
        rm .pids
    fi
    echo "✅ All services stopped"
    exit 0
}

# Set trap to clean up on exit
trap cleanup EXIT INT TERM

# Keep script running
wait
