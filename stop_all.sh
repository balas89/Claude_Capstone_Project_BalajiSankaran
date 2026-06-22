#!/bin/bash

# Multi-Agent Loan Approval System - Stop All Services Script

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║   Stopping Multi-Agent Loan Approval System                   ║"
echo "╚════════════════════════════════════════════════════════════════╝"

# Stop services from PID file if it exists
if [ -f .pids ]; then
    echo ""
    echo "Stopping services using PID file..."
    while IFS= read -r pid; do
        if kill -0 "$pid" 2>/dev/null; then
            echo "Stopping process $pid..."
            kill "$pid"
        fi
    done < .pids
    rm .pids
    echo "All services stopped!"
else
    # Alternative: kill by port
    echo ""
    echo "PID file not found. Stopping services by port..."

    echo "Stopping Applicant DB (port 8001)..."
    lsof -ti:8001 | xargs kill -9 2>/dev/null || true

    echo "Stopping Risk Rules DB (port 8002)..."
    lsof -ti:8002 | xargs kill -9 2>/dev/null || true

    echo "Stopping Decision Synthesis (port 8003)..."
    lsof -ti:8003 | xargs kill -9 2>/dev/null || true

    echo "Stopping Notification System (port 8004)..."
    lsof -ti:8004 | xargs kill -9 2>/dev/null || true

    echo "Stopping FastAPI (port 8000)..."
    lsof -ti:8000 | xargs kill -9 2>/dev/null || true

    echo "Stopping Streamlit (port 8501)..."
    lsof -ti:8501 | xargs kill -9 2>/dev/null || true

    echo "Services stopped!"
fi

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                ✅ ALL SERVICES STOPPED ✅                     ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
