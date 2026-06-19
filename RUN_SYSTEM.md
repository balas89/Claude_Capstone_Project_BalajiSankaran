# 🚀 Running the Loan Approval System - Complete Guide

## Prerequisites ✅

- [x] ANTHROPIC_API_KEY environment variable set
- [x] Python 3.8+ installed
- [x] Dependencies installed via virtual environment

---

## Method 1: Using Individual Terminals (Recommended for Development)

This method gives you full visibility into each service's logs.

### Step 1: Navigate to Project Directory

```bash
cd /home/ubuntu/Desktop/Capstone_project_3
```

### Step 2: Activate Virtual Environment (All Terminals)

In each terminal you open, first activate the virtual environment:

```bash
source venv/bin/activate
```

You should see `(venv)` prefix in your terminal.

### Step 3: Start Each Service in Separate Terminal

**Terminal 1 - Applicant DB MCP Server (Port 8001)**
```bash
source venv/bin/activate
python3 -m mcp_servers.applicant_db
```
Expected output:
```
INFO:     Uvicorn running on http://0.0.0.0:8001
INFO:     Application startup complete
```

**Terminal 2 - Risk Rules DB MCP Server (Port 8002)**
```bash
source venv/bin/activate
python3 -m mcp_servers.risk_rules_db
```
Expected output:
```
INFO:     Uvicorn running on http://0.0.0.0:8002
INFO:     Application startup complete
```

**Terminal 3 - Decision Synthesis MCP Server (Port 8003)**
```bash
source venv/bin/activate
python3 -m mcp_servers.decision_synthesis
```
Expected output:
```
INFO:     Uvicorn running on http://0.0.0.0:8003
INFO:     Application startup complete
```

**Terminal 4 - Notification System MCP Server (Port 8004)**
```bash
source venv/bin/activate
python3 -m mcp_servers.notification_system
```
Expected output:
```
INFO:     Uvicorn running on http://0.0.0.0:8004
INFO:     Application startup complete
```

**Terminal 5 - FastAPI Microservice (Port 8000)**
```bash
source venv/bin/activate
python3 -m microservices.app
```
Expected output:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

**Terminal 6 - Streamlit UI (Port 8501)**
```bash
source venv/bin/activate
streamlit run ui/streamlit_app.py
```
Expected output:
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

### Step 4: Access the UI

Open your browser and navigate to:
```
http://localhost:8501
```

---

## Method 2: Using Startup Script (Linux/Mac)

For convenience, use the provided startup script:

```bash
cd /home/ubuntu/Desktop/Capstone_project_3
chmod +x start_all.sh
./start_all.sh
```

The script will:
1. Activate the virtual environment
2. Load environment variables from .env
3. Start all MCP servers (background)
4. Start FastAPI microservice (background)
5. Start Streamlit UI (foreground)

Press `Ctrl+C` to stop all services.

---

## Method 3: Using Startup Script (Windows)

For Windows users:

```bash
cd C:\Users\YourUser\Desktop\Capstone_project_3
start_all.bat
```

This will open separate command windows for each service.

---

## 🧪 Testing the System

### Option A: Using Streamlit UI (Easiest)

1. Navigate to http://localhost:8501
2. Fill out the loan application form:
   - Applicant ID: `TEST_001`
   - Age: 35
   - Income: $100,000
   - Employment Type: Salaried
   - Credit Score: 750
   - Loan Amount: $80,000
   - Tenure: 60 months
   - Existing Liabilities: $5,000
   - Location: New York

3. Click "Submit Application"
4. Wait for processing (5-15 seconds for first request)
5. View the decision and analysis

### Option B: Using Python Test Script

```bash
cd /home/ubuntu/Desktop/Capstone_project_3
source venv/bin/activate
python3 test_api.py
```

Expected output:
```
Testing Health Check Endpoint
✅ Health check passed

Testing Loan Application: approval_case
✅ Application processed successfully
Decision: Approve
Risk Score: 25.00%
Confidence: 85.00%
Case ID: CASE_TEST_APPROVAL_001_...

TEST SUMMARY
✅ approval_case: Approve
✅ rejection_case: Reject
✅ review_case: Requires Manual Review
```

### Option C: Using curl

```bash
curl -X POST http://localhost:8000/apply-loan \
  -H "Content-Type: application/json" \
  -d '{
    "applicant_id": "CURL_TEST",
    "age": 35,
    "income": 100000,
    "employment_type": "Salaried",
    "credit_score": 750,
    "loan_amount": 80000,
    "tenure_months": 60,
    "existing_liabilities": 5000,
    "location": "New York"
  }'
```

Expected response:
```json
{
  "case_id": "CASE_CURL_TEST_20240115...",
  "applicant_id": "CURL_TEST",
  "decision": "Approve",
  "risk_score": 0.25,
  "confidence": 0.85,
  "factors": ["Good credit score", "Stable employment", ...],
  "explanation": "...",
  "profile_analysis": {...},
  "financial_analysis": {...},
  "compliance_status": {...},
  "timestamp": "2024-01-15T10:15:00.123456"
}
```

---

## 🔍 Verifying Services Are Running

Check each service is accessible:

```bash
# Check Applicant DB
curl http://localhost:8001/health

# Check Risk Rules DB
curl http://localhost:8002/health

# Check Decision Synthesis
curl http://localhost:8003/health

# Check Notification System
curl http://localhost:8004/health

# Check FastAPI Microservice
curl http://localhost:8000/health
```

Expected response for all:
```json
{"status": "healthy", "timestamp": "2024-01-15T10:15:00.123456"}
```

---

## 📊 Streamlit UI Features

Once the UI is open at http://localhost:8501:

### Application Form
- Fill in loan applicant details
- All fields are validated in real-time
- Submit button becomes active when form is valid

### Decision Results
- Decision badge (✅ APPROVED / ❌ REJECTED / ⚠️ REQUIRES MANUAL REVIEW)
- Risk Score (0-100%)
- Confidence Level (0-100%)
- Case ID for tracking

### Analysis Tabs
1. **Profile Analysis**
   - Income stability score
   - Employment risk level
   - Credit history details
   - Completeness flags

2. **Financial Analysis**
   - Debt-to-Income ratio
   - Credit risk level
   - Loan amount risk
   - Detected anomalies

3. **Compliance**
   - Action taken
   - Notification status
   - Timestamp

4. **Full Details**
   - Complete JSON response

### Application History
- Session-based history of submitted applications
- Shows decision, case ID, risk score

---

## 🐛 Troubleshooting

### Issue: "Connection refused" on localhost:8501

**Solution**: 
- Ensure Streamlit is running: `streamlit run ui/streamlit_app.py`
- Check port 8501 is not blocked
- Wait 5 seconds after starting for Streamlit to initialize

### Issue: MCP Server won't start

**Solution**:
```bash
# Check if port is already in use
lsof -i :8001  # Replace with your port
lsof -i :8002
# etc.

# Kill existing process if needed
kill -9 <PID>
```

### Issue: "ANTHROPIC_API_KEY not found"

**Solution**:
```bash
# Set API key in current terminal
export ANTHROPIC_API_KEY="sk-ant-..."

# Verify it's set
echo $ANTHROPIC_API_KEY

# Or add to .env file
echo "ANTHROPIC_API_KEY=sk-ant-..." >> .env
source venv/bin/activate
```

### Issue: Timeout errors

**Solution**:
- First request takes 5-15 seconds (Claude API latency) - this is normal
- Subsequent requests should be 2-5 seconds
- Check your internet connection
- Verify ANTHROPIC_API_KEY is valid

### Issue: ModuleNotFoundError

**Solution**:
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: Port already in use

**Solution**:
```bash
# Find which process is using the port
lsof -i :8000
lsof -i :8501

# Kill the process
kill -9 <PID>

# Or change port in .env
FASTAPI_PORT=8001  # Use different port
```

---

## 📚 API Documentation

Once FastAPI is running, access interactive documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These provide:
- Interactive API testing
- Complete endpoint documentation
- Request/response schemas
- Try-it-out functionality

---

## 📈 Performance Notes

### First Request
- Takes 5-15 seconds
- This is due to Claude API latency and initial compilation
- This is normal behavior

### Subsequent Requests
- Typically 2-5 seconds
- Much faster as models are cached

### Concurrent Requests
- System can handle 10+ concurrent requests
- All MCP servers run independently
- Orchestration coordinates properly

---

## 🔐 Security Reminders

- **Never commit .env with your API key** to version control
- Use `.env.example` as template
- Rotate API keys regularly
- Monitor API usage for unexpected costs

---

## 📝 Logging & Debugging

### View MCP Server Logs
```bash
# Terminal with each MCP server shows:
# - Request timestamps
# - Processing details
# - Any errors or warnings
```

### View FastAPI Logs
```bash
# Terminal with FastAPI shows:
# - HTTP request methods and paths
# - Status codes
# - Response times
```

### View Streamlit Logs
```bash
# Terminal with Streamlit shows:
# - Session events
# - Widget interactions
# - Reruns and updates
```

### Check Application Decision Logs
Visit http://localhost:8004/audit_trail to see all decisions logged.

---

## ✅ Verification Checklist

Before considering the system fully operational:

- [ ] All 6 services started without errors
- [ ] Health checks pass for all 4 MCP servers
- [ ] FastAPI /docs endpoint is accessible
- [ ] Streamlit UI loads at localhost:8501
- [ ] Test application processes successfully
- [ ] Decision is displayed with reasoning
- [ ] Analysis tabs show detailed information
- [ ] No error messages in any terminal

---

## 🎯 Next Steps

1. ✅ Start all services using one of the three methods above
2. ✅ Open Streamlit UI at http://localhost:8501
3. ✅ Submit a test loan application
4. ✅ Review the decision and analysis
5. ✅ Try different test cases (approval, rejection, review)
6. ✅ Test with curl or Python script
7. ✅ Review API documentation at http://localhost:8000/docs

---

## 📞 Support

If you encounter issues:

1. Check this RUN_SYSTEM.md file first
2. Review QUICKSTART.md for setup guidance
3. Check TESTING_GUIDE.md for testing strategies
4. Review ARCHITECTURE.md for system design
5. Check logs in each terminal for error details

---

## 🎉 You're Ready!

The system is now ready to use. Start with the **Individual Terminals method** for best visibility into what's happening.

Good luck! 🚀
