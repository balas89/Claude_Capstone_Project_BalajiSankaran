@echo off
REM Start all services for the Loan Approval System (Windows)

setlocal enabledelayedexpansion

echo.
echo ===============================================
echo   Loan Approval System - Startup Script
echo ===============================================
echo.

REM Check if virtual environment exists
if exist "venv" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo WARNING: Virtual environment not found
    echo Create with: python -m venv venv
)

REM Load environment variables from .env
if exist ".env" (
    echo Loading environment variables from .env
    for /f "delims== tokens=1,2" %%a in (.env) do (
        if not "%%a"=="" if not "!%%a:~0,1!"=="#" set %%a=%%b
    )
) else (
    echo WARNING: .env file not found
    echo Copy from .env.example: copy .env.example .env
)

echo.
echo ===============================================
echo   Starting MCP Servers...
echo ===============================================
echo.

echo Starting Applicant DB MCP Server (port 8001)...
start "Applicant DB MCP" python -m mcp_servers.applicant_db
timeout /t 2 /nobreak

echo Starting Risk Rules DB MCP Server (port 8002)...
start "Risk Rules DB MCP" python -m mcp_servers.risk_rules_db
timeout /t 2 /nobreak

echo Starting Decision Synthesis MCP Server (port 8003)...
start "Decision Synthesis MCP" python -m mcp_servers.decision_synthesis
timeout /t 2 /nobreak

echo Starting Notification System MCP Server (port 8004)...
start "Notification System MCP" python -m mcp_servers.notification_system
timeout /t 3 /nobreak

echo.
echo ===============================================
echo   Starting FastAPI Microservice...
echo ===============================================
echo.

start "FastAPI Microservice" python -m microservices.app
timeout /t 2 /nobreak

echo.
echo ===============================================
echo   Starting Streamlit UI...
echo ===============================================
echo.

start "Streamlit UI" streamlit run ui/streamlit_app.py

echo.
echo ===============================================
echo   All Services Started!
echo ===============================================
echo.
echo Service URLs:
echo   Applicant DB MCP:        http://localhost:8001
echo   Risk Rules DB MCP:       http://localhost:8002
echo   Decision Synthesis MCP:  http://localhost:8003
echo   Notification System MCP: http://localhost:8004
echo   FastAPI Microservice:    http://localhost:8000
echo   Streamlit UI:            http://localhost:8501
echo.
echo API Documentation: http://localhost:8000/docs
echo.
pause
