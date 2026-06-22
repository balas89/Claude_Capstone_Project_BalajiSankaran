@echo off
REM Multi-Agent Loan Approval System - Stop All Services Script (Windows)

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║   Stopping Multi-Agent Loan Approval System                   ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

echo Stopping services by port...

echo Stopping Applicant DB (port 8001)...
netstat -ano | findstr :8001 | for /f "tokens=5" %%a in ('findstr :8001') do taskkill /pid %%a /f 2>nul

echo Stopping Risk Rules DB (port 8002)...
netstat -ano | findstr :8002 | for /f "tokens=5" %%a in ('findstr :8002') do taskkill /pid %%a /f 2>nul

echo Stopping Decision Synthesis (port 8003)...
netstat -ano | findstr :8003 | for /f "tokens=5" %%a in ('findstr :8003') do taskkill /pid %%a /f 2>nul

echo Stopping Notification System (port 8004)...
netstat -ano | findstr :8004 | for /f "tokens=5" %%a in ('findstr :8004') do taskkill /pid %%a /f 2>nul

echo Stopping FastAPI (port 8000)...
netstat -ano | findstr :8000 | for /f "tokens=5" %%a in ('findstr :8000') do taskkill /pid %%a /f 2>nul

echo Stopping Streamlit (port 8501)...
netstat -ano | findstr :8501 | for /f "tokens=5" %%a in ('findstr :8501') do taskkill /pid %%a /f 2>nul

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                ✅ ALL SERVICES STOPPED ✅                     ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

pause
