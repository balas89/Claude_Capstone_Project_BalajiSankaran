# 🏦 Multi-Agent Agentic AI Loan Approval System

An end-to-end intelligent loan approval system using multiple specialized AI agents coordinated through LangGraph, with real-time decision synthesis using Claude API.

## 🏗️ System Architecture

### Layer 1: Presentation (Streamlit)
- Interactive chatbot UI for loan applications
- Real-time decision display with explanations
- Audit trail and decision history

### Layer 2: Microservices (FastAPI)
- REST API endpoints for loan application processing
- Request validation and health checks

### Layer 3: Orchestration (LangGraph)
- Workflow coordinator managing agent sequences
- State management for application lifecycle
- Error handling and fallback mechanisms

### Layer 4: Agents & MCP Servers
1. **Applicant Profile Agent** - Analyzes applicant details, credit history, employment verification
2. **Financial Risk Agent** - Calculates DTI, credit risk, loan amount risk
3. **Loan Decision Agent** - Uses Claude Sonnet to synthesize final decision
4. **Compliance Agent** - Executes compliance checks and notifications

### Layer 5: Data Layer
- Mock credit history database
- Mock employment verification system
- Mock compliance rules engine
- Audit trail and notification service

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- ANTHROPIC_API_KEY environment variable set

### Installation

1. Clone or download the project:
```bash
cd /home/ubuntu/Desktop/Capstone_project_3
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### Running the System

The system consists of multiple services that should run in separate terminal windows:

#### Terminal 1: MCP Server 1 - Applicant DB
```bash
cd /home/ubuntu/Desktop/Capstone_project_3
source venv/bin/activate
python -m mcp_servers.applicant_db
# Server running on http://localhost:8001
```

#### Terminal 2: MCP Server 2 - Risk Rules DB
```bash
cd /home/ubuntu/Desktop/Capstone_project_3
source venv/bin/activate
python -m mcp_servers.risk_rules_db
# Server running on http://localhost:8002
```

#### Terminal 3: MCP Server 3 - Decision Synthesis
```bash
cd /home/ubuntu/Desktop/Capstone_project_3
source venv/bin/activate
python -m mcp_servers.decision_synthesis
# Server running on http://localhost:8003
```

#### Terminal 4: MCP Server 4 - Notification System
```bash
cd /home/ubuntu/Desktop/Capstone_project_3
source venv/bin/activate
python -m mcp_servers.notification_system
# Server running on http://localhost:8004
```

#### Terminal 5: FastAPI Microservice
```bash
cd /home/ubuntu/Desktop/Capstone_project_3
source venv/bin/activate
python -m microservices.app
# API running on http://localhost:8000
# Visit http://localhost:8000/docs for Swagger UI
```

#### Terminal 6: Streamlit UI
```bash
cd /home/ubuntu/Desktop/Capstone_project_3
source venv/bin/activate
streamlit run ui/streamlit_app.py
# UI running on http://localhost:8501
```

### Quick Start Script

Create a shell script to start all services at once:

```bash
#!/bin/bash
# start_all.sh

source venv/bin/activate

# Start MCP servers in background
python -m mcp_servers.applicant_db &
python -m mcp_servers.risk_rules_db &
python -m mcp_servers.decision_synthesis &
python -m mcp_servers.notification_system &

# Start FastAPI microservice in background
python -m microservices.app &

# Start Streamlit UI in foreground
streamlit run ui/streamlit_app.py

# Cleanup on exit
trap "kill %1 %2 %3 %4 %5" EXIT
```

## 📊 Workflow

```
User Application (Streamlit UI)
    ↓
FastAPI Microservice (/apply-loan endpoint)
    ↓
LangGraph Orchestration Engine
    ├→ Applicant Profile Agent → MCP: ApplicantDB
    ├→ Financial Risk Agent → MCP: RiskRulesDB
    ├→ Loan Decision Agent (Claude) → MCP: DecisionSynthesis
    └→ Compliance Agent → MCP: NotificationSystem
    ↓
Decision Response (Streamlit UI Display)
```

## 🧪 Test Cases

### Test 1: Likely Approval
```json
{
  "applicant_id": "APP_TEST_001",
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

### Test 2: Likely Rejection
```json
{
  "applicant_id": "APP_TEST_002",
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

### Test 3: Manual Review
```json
{
  "applicant_id": "APP_TEST_003",
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

### Using cURL to Test
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

## 📁 Project Structure

```
Capstone_project_3/
├── mcp_servers/
│   ├── applicant_db.py          # Applicant profile MCP server
│   ├── risk_rules_db.py         # Risk analysis MCP server
│   ├── decision_synthesis.py    # Decision synthesis with Claude
│   └── notification_system.py   # Compliance & notifications
├── agents/
│   ├── applicant_agent.py       # Applicant analysis agent
│   ├── financial_risk_agent.py  # Financial risk agent
│   ├── loan_decision_agent.py   # LLM-based decision agent
│   └── compliance_agent.py      # Compliance orchestrator
├── orchestration/
│   ├── workflow.py              # LangGraph workflow
│   └── state.py                 # State management
├── microservices/
│   ├── app.py                   # FastAPI main app
│   ├── schemas.py               # Pydantic models
│   └── routes.py                # API routes
├── ui/
│   └── streamlit_app.py         # Streamlit UI
├── utils/
│   ├── config.py                # Configuration
│   └── mock_data.py             # Mock databases
├── requirements.txt
├── .env.example
└── README.md
```

## 🔧 Configuration

Edit `utils/config.py` to adjust:
- Loan thresholds (min income, max loan, etc.)
- Risk thresholds
- Service URLs
- API model selection

## 📝 Decision Factors

The system considers:
- Credit score and payment history
- Debt-to-income ratio
- Income stability and employment verification
- Existing liabilities
- Loan amount relative to income
- Tenure and payment capacity
- Regulatory compliance requirements

## 🎯 Key Features

✅ **Multi-Agent Architecture** - Independent agents for different analysis domains
✅ **LLM Integration** - Claude API for final decision synthesis
✅ **Explainability** - Every decision includes reasoning and factors
✅ **Audit Trail** - Complete logging of all decisions
✅ **Compliance** - Regulatory checks and notifications
✅ **Scalability** - Microservices can scale independently
✅ **Real-time Processing** - Immediate loan decisions
✅ **User-Friendly UI** - Streamlit chatbot interface

## 🐛 Troubleshooting

### "Cannot connect to API"
- Ensure FastAPI microservice is running on port 8000
- Check that all MCP servers are running

### "Timeout errors"
- Verify ANTHROPIC_API_KEY is set correctly
- Check API rate limits
- Ensure sufficient network connectivity

### "Port already in use"
- Change port in .env file
- Or kill existing process: `lsof -ti:8000 | xargs kill -9`

## 📚 API Documentation

Once FastAPI is running, view interactive documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🚀 Performance Notes

- First decision may take 5-15 seconds (Claude API latency)
- Subsequent requests typically process in 2-5 seconds
- System can handle concurrent applications
- Mock databases respond instantly

## 📋 License

This project is provided as-is for educational and evaluation purposes.

## 🤝 Support

For issues or questions, check the logs from each service for detailed error messages.
