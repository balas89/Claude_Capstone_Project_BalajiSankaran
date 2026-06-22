@echo off
REM Multi-Agent Loan Approval System - All Services Startup Script (Windows)
REM Run with: run_all.bat

setlocal enabledelayedexpansion

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║   Starting Multi-Agent Loan Approval System                   ║
echo ║   All 6 Services (Windows)                                    ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Create logs directory
if not exist logs mkdir logs

echo.
echo Starting all services...
echo.

REM Start all services in new windows
echo [1/6] Starting Applicant DB MCP (Port 8001)...
start "Applicant DB MCP" cmd /k "python -m uvicorn mcp_servers.applicant_db:app --host 0.0.0.0 --port 8001 --reload"

timeout /t 1 /nobreak

echo [2/6] Starting Risk Rules DB MCP (Port 8002)...
start "Risk Rules DB MCP" cmd /k "python -m uvicorn mcp_servers.risk_rules_db:app --host 0.0.0.0 --port 8002 --reload"

timeout /t 1 /nobreak

echo [3/6] Starting Decision Synthesis MCP (Port 8003)...
start "Decision Synthesis MCP" cmd /k "python -m uvicorn mcp_servers.decision_synthesis:app --host 0.0.0.0 --port 8003 --reload"

timeout /t 1 /nobreak

echo [4/6] Starting Notification System MCP (Port 8004)...
start "Notification System MCP" cmd /k "python -m uvicorn mcp_servers.notification_system:app --host 0.0.0.0 --port 8004 --reload"

timeout /t 1 /nobreak

echo [5/6] Starting FastAPI Microservice (Port 8000)...
start "FastAPI Service" cmd /k "python -m uvicorn microservices.app:app --host 0.0.0.0 --port 8000 --reload"

timeout /t 1 /nobreak

echo [6/6] Starting Streamlit UI (Port 8501)...
start "Streamlit UI" cmd /k "streamlit run ui/streamlit_app.py --server.port 8501 --logger.level=debug"

timeout /t 3 /nobreak

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                   ✅ ALL SERVICES STARTED ✅                  ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo Services running:
echo   ✓ Applicant DB MCP:        http://localhost:8001
echo   ✓ Risk Rules DB MCP:       http://localhost:8002
echo   ✓ Decision Synthesis MCP:  http://localhost:8003
echo   ✓ Notification System MCP: http://localhost:8004
echo   ✓ FastAPI Service:         http://localhost:8000
echo   ✓ Streamlit UI:            http://localhost:8501 ← OPEN THIS
echo.
echo API Documentation: http://localhost:8000/docs
echo.
echo Opening browser...
timeout /t 2 /nobreak

REM Open browser
start http://localhost:8501

echo.
echo All services are running in separate windows.
echo Close any window to stop that service.
echo.
pause
