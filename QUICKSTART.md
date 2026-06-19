# 🚀 Quick Start Guide

## 5-Minute Setup

### Step 1: Set API Key (Required)
```bash
export ANTHROPIC_API_KEY="sk-ant-..." # Your Anthropic API key
```

Or create `.env` file:
```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### Step 2: Install Dependencies
```bash
python3 -m pip install --user fastapi uvicorn anthropic pydantic python-dotenv streamlit requests langchain
```

### Step 3: Run Individual Services (Recommended for Development)

Open 6 terminals and run each command:

**Terminal 1 - Applicant DB MCP Server (Port 8001)**
```bash
cd /home/ubuntu/Desktop/Capstone_project_3
python3 -m mcp_servers.applicant_db
```

**Terminal 2 - Risk Rules DB MCP Server (Port 8002)**
```bash
cd /home/ubuntu/Desktop/Capstone_project_3
python3 -m mcp_servers.risk_rules_db
```

**Terminal 3 - Decision Synthesis MCP Server (Port 8003)**
```bash
cd /home/ubuntu/Desktop/Capstone_project_3
python3 -m mcp_servers.decision_synthesis
```

**Terminal 4 - Notification System MCP Server (Port 8004)**
```bash
cd /home/ubuntu/Desktop/Capstone_project_3
python3 -m mcp_servers.notification_system
```

**Terminal 5 - FastAPI Microservice (Port 8000)**
```bash
cd /home/ubuntu/Desktop/Capstone_project_3
python3 -m microservices.app
```

**Terminal 6 - Streamlit UI (Port 8501)**
```bash
cd /home/ubuntu/Desktop/Capstone_project_3
streamlit run ui/streamlit_app.py
```

### Step 4: Access the UI
Open browser to: **http://localhost:8501**

---

## 🎯 Test the System

### Option A: Using Streamlit UI (Easiest)
1. Go to http://localhost:8501
2. Fill out the loan application form
3. Click "Submit Application"
4. View the decision and detailed analysis

### Option B: Using curl (API Testing)
```bash
curl -X POST http://localhost:8000/apply-loan \
  -H "Content-Type: application/json" \
  -d '{
    "applicant_id": "TEST_001",
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

### Option C: Using Python Test Script
```bash
python3 test_api.py
```

---

## 📊 System Workflow

```
Streamlit UI
    ↓
FastAPI (Port 8000)
    ├→ Applicant Profile Agent → MCP Server 8001
    ├→ Financial Risk Agent → MCP Server 8002
    ├→ Loan Decision Agent (Claude) → MCP Server 8003
    └→ Compliance Agent → MCP Server 8004
    ↓
Decision Display
```

---

## 🧪 Test Cases

### Likely Approval
```json
{
  "applicant_id": "APP_GOOD",
  "age": 35,
  "income": 120000,
  "employment_type": "Salaried",
  "credit_score": 780,
  "loan_amount": 100000,
  "tenure_months": 60,
  "existing_liabilities": 10000,
  "location": "New York"
}
```

### Likely Rejection
```json
{
  "applicant_id": "APP_BAD",
  "age": 25,
  "income": 25000,
  "employment_type": "Self-Employed",
  "credit_score": 550,
  "loan_amount": 300000,
  "tenure_months": 120,
  "existing_liabilities": 80000,
  "location": "California"
}
```

### Likely Manual Review
```json
{
  "applicant_id": "APP_MIXED",
  "age": 45,
  "income": 75000,
  "employment_type": "Salaried",
  "credit_score": 680,
  "loan_amount": 150000,
  "tenure_months": 84,
  "existing_liabilities": 35000,
  "location": "Texas"
}
```

---

## 🔍 API Documentation

After starting the FastAPI service, view interactive docs:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| "Cannot connect to API" | Ensure FastAPI is running on port 8000 |
| "Timeout errors" | Check ANTHROPIC_API_KEY is set and valid |
| "Port already in use" | Change port in .env or kill existing process |
| "ModuleNotFoundError" | Run from project directory and install dependencies |
| "MCP Server not responding" | Ensure all 4 MCP servers are running on ports 8001-8004 |

---

## 📝 Expected Output

When you submit a loan application, you should see:

```
✅ APPROVED (or ❌ REJECTED or ⚠️ REQUIRES MANUAL REVIEW)

Risk Score: 25%
Confidence: 85%
Case ID: CASE_APP001_...

Decision Explanation:
[Claude-generated explanation of the decision]

Key Decision Factors:
• Strong income stability
• Good credit score
• Reasonable DTI ratio
• [More factors...]
```

---

## 🎓 Understanding the System

### Agents
1. **Applicant Profile Agent**: Analyzes demographics, employment, credit
2. **Financial Risk Agent**: Calculates DTI, detects anomalies
3. **Loan Decision Agent**: Uses Claude to synthesize final decision
4. **Compliance Agent**: Executes compliance checks

### MCP Servers (Model Context Protocol)
- Independent services providing specialized data
- RESTful interfaces for agent communication
- Mock databases with realistic loan evaluation logic

### Orchestration (LangGraph)
- Coordinates agent workflow
- Manages state transitions
- Handles error cases

---

## 🚀 Production Considerations

- Replace mock databases with real APIs
- Add authentication (JWT, OAuth)
- Implement rate limiting
- Add comprehensive logging
- Use Docker containers
- Deploy on Kubernetes
- Add monitoring and alerts

---

## 📚 Project Structure

```
├── mcp_servers/          # 4 MCP servers providing data
├── agents/               # 4 domain-specific agents
├── orchestration/        # LangGraph workflow
├── microservices/        # FastAPI app
├── ui/                   # Streamlit chatbot
├── utils/                # Config and mock data
├── test_api.py           # API test script
├── start_all.sh          # Start all services (Linux/Mac)
├── start_all.bat         # Start all services (Windows)
├── requirements.txt      # Python dependencies
├── .env.example          # Environment template
├── QUICKSTART.md         # This file
└── README.md             # Full documentation
```

---

## 💡 Tips

- First decision may take 5-15s (Claude API latency)
- Subsequent requests typically process in 2-5s
- View Streamlit logs for real-time processing updates
- Check MCP server logs for data analysis details
- Use curl or Postman for API testing
- Review audit trail in Notification System logs

---

Need help? Check the main README.md for detailed documentation.
