# Project Structure: Detailed File-by-File Breakdown

## 📂 Directory Tree with Descriptions

```
Capstone_project_3/
│
├── 🤖 AGENTS LAYER (Multi-Agent AI System)
│   ├── agents/
│   │   ├── __init__.py
│   │   │   └─ Purpose: Package initialization
│   │   │
│   │   ├── applicant_agent.py (Agent 1)
│   │   │   └─ 🎯 Analyzes applicant profile and personal data
│   │   │       Input: LoanApplication (ID, age, income, employment, etc.)
│   │   │       Output: ApplicantProfileResult
│   │   │       Tasks:
│   │   │         • Validate data completeness
│   │   │         • Calculate income stability score
│   │   │         • Assess employment risk (Low/Medium/High)
│   │   │         • Summarize credit history
│   │   │         • Flag data quality issues
│   │   │
│   │   ├── financial_risk_agent.py (Agent 2)
│   │   │   └─ 🎯 Evaluates financial metrics and risk
│   │   │       Input: LoanApplication
│   │   │       Output: FinancialRiskResult
│   │   │       Tasks:
│   │   │         • Calculate DTI ratio (monthly debt/income)
│   │   │         • Determine credit risk level
│   │   │         • Calculate loan-to-income ratio
│   │   │         • Detect financial anomalies
│   │   │         • Provide financial reasoning
│   │   │
│   │   ├── loan_decision_agent.py (Agent 3)
│   │   │   └─ 🎯 Synthesizes final decision from all analyses
│   │   │       Input: Application + Results from Agent 1 & 2
│   │   │       Output: LoanDecisionResult
│   │   │       Tasks:
│   │   │         • Call business rules engine
│   │   │         • Make decision: Approve/Reject/Manual Review
│   │   │         • Calculate risk score
│   │   │         • Generate explanation with Claude
│   │   │
│   │   └── compliance_agent.py (Agent 4)
│   │       └─ 🎯 Ensures compliance and handles notifications
│   │           Input: Application + Decision result
│   │           Output: ComplianceResult
│   │           Tasks:
│   │             • Validate regulatory compliance
│   │             • Send notifications
│   │             • Record audit trail
│   │             • Log decision for records
│   │
├── 🔌 MCP SERVERS (Independent Microservices)
│   ├── mcp_servers/
│   │   ├── applicant_db.py (MCP Server 1 - Port 8001)
│   │   │   └─ 🎯 Applicant Data Service
│   │   │       GET /health
│   │   │       POST /get_applicant_profile
│   │   │       Provides:
│   │   │         • Credit history database queries
│   │   │         • Employment verification
│   │   │         • Income stability calculations
│   │   │         • Mock applicant data
│   │   │
│   │   ├── risk_rules_db.py (MCP Server 2 - Port 8002)
│   │   │   └─ 🎯 Financial Risk Rules Service
│   │   │       GET /health
│   │   │       POST /analyze_financial_risk
│   │   │       Provides:
│   │   │         • DTI/LTI calculations
│   │   │         • Loan amount risk assessment
│   │   │         • Anomaly detection
│   │   │         • Risk scoring
│   │   │
│   │   ├── decision_synthesis.py (MCP Server 3 - Port 8003)
│   │   │   └─ 🎯 Decision Synthesis Service
│   │   │       GET /health
│   │   │       POST /synthesize_decision
│   │   │       Provides:
│   │   │         • Business rules engine (NOT LLM-based)
│   │   │         • Approve/Reject/Manual Review decision
│   │   │         • Risk score calculation
│   │   │         • Claude-enhanced explanation
│   │   │
│   │   └── notification_system.py (MCP Server 4 - Port 8004)
│   │       └─ 🎯 Notification & Audit Service
│   │           GET /health
│   │           POST /notify
│   │           POST /log_decision
│   │           Provides:
│   │             • Notification sending (mock)
│   │             • Audit trail logging
│   │             • Decision recording
│   │             • Case tracking
│   │
├── 🌐 MICROSERVICES (FastAPI Layer)
│   ├── microservices/
│   │   ├── app.py
│   │   │   └─ 🎯 FastAPI Application Setup
│   │   │       Creates FastAPI instance
│   │   │       Configures CORS (for Streamlit)
│   │   │       Initializes LoanApprovalWorkflow
│   │   │       Runs on: http://localhost:8000
│   │   │
│   │   ├── schemas.py
│   │   │   └─ 🎯 Pydantic Models (Data Validation)
│   │   │       Models:
│   │   │         • LoanApplication (input schema)
│   │   │         • ApplicantProfileResult (Agent 1 output)
│   │   │         • FinancialRiskResult (Agent 2 output)
│   │   │         • LoanDecisionResult (Agent 3 output)
│   │   │         • ComplianceResult (Agent 4 output)
│   │   │         • LoanDecisionResponse (API response)
│   │   │         • HealthCheck (health status)
│   │   │       Features:
│   │   │         • Type validation
│   │   │         • Range checking
│   │   │         • Required field enforcement
│   │   │
│   │   └── routes.py
│   │       └─ 🎯 REST API Endpoints
│   │           POST /apply-loan
│   │             → Receives LoanApplication JSON
│   │             → Calls LangGraph orchestration
│   │             → Returns LoanDecisionResponse JSON
│   │           GET /health
│   │             → Returns service health status
│   │             → Used by docker-compose health checks
│   │
├── 🔗 ORCHESTRATION (LangGraph Workflow)
│   ├── orchestration/
│   │   ├── state.py
│   │   │   └─ 🎯 Workflow State Definition
│   │   │       Defines:
│   │   │         • ApplicationState (input structure)
│   │   │         • WorkflowState (complete state)
│   │   │       Fields tracked:
│   │   │         • application (LoanApplication)
│   │   │         • case_id (unique identifier)
│   │   │         • Profile/Financial/Decision/Compliance results
│   │   │         • current_step (workflow progress)
│   │   │         • errors (error tracking)
│   │   │         • processing_complete (status flag)
│   │   │
│   │   └── workflow.py
│   │       └─ 🎯 LangGraph Orchestration Engine
│   │           Class: LoanApprovalWorkflow
│   │           Methods:
│   │             • __init__: Create agents
│   │             • _build_graph: Define workflow edges
│   │             • _initialize_state: Setup
│   │             • _analyze_applicant_profile: Agent 1 node
│   │             • _analyze_financial_risk: Agent 2 node
│   │             • _synthesize_decision: Agent 3 node
│   │             • _execute_compliance: Agent 4 node
│   │             • _finalize_state: Cleanup
│   │             • process_application: Main method
│   │             • _build_response_from_graph_state: Response conversion
│   │
│   │           Workflow Graph:
│   │             initialize
│   │                 ↓
│   │           ┌─────┴─────┐
│   │           ↓           ↓      (Parallel)
│   │         Agent1     Agent2
│   │           ↓           ↓
│   │           └─────┬─────┘
│   │                 ↓
│   │              Agent3
│   │                 ↓
│   │              Agent4
│   │                 ↓
│   │             finalize
│   │
├── 🎨 USER INTERFACE
│   ├── ui/
│   │   └── streamlit_app.py
│   │       └─ 🎯 Streamlit Chatbot Interface
│   │           Components:
│   │             • Application Form (9 fields)
│   │             • Decision Results Display
│   │             • Metrics Dashboard
│   │             • Detailed Analysis Tabs
│   │             • Application History
│   │             • Service Health Monitor
│   │           Features:
│   │             • Real-time decision display
│   │             • Color-coded results
│   │             • Session state management
│   │             • Multiple applications support
│   │           API Integration:
│   │             • Calls http://localhost:8000/apply-loan
│   │             • Displays results
│   │             • Maintains application history
│   │
├── 🛠️ UTILITIES
│   ├── utils/
│   │   ├── config.py
│   │   │   └─ 🎯 Configuration Management
│   │   │       Manages:
│   │   │         • ANTHROPIC_API_KEY (from .env)
│   │   │         • Model name (Claude Sonnet 4.6)
│   │   │         • Port configurations
│   │   │         • MCP server URLs
│   │   │         • Logging setup
│   │   │
│   │   ├── decision_rules.py (255 lines)
│   │   │   └─ 🎯 Business Rules Engine (Core Logic)
│   │   │       Class: LoanDecisionRules
│   │   │       Methods:
│   │   │         • make_decision() → (decision, risk_score, reasoning)
│   │   │         • calculate_risk_score() → 0.0-1.0
│   │   │       Decision Rules:
│   │   │         HARD REJECTIONS:
│   │   │           • DTI ≥ 50% → REJECT
│   │   │           • Credit < 600 → REJECT
│   │   │           • 2+ severe anomalies → REJECT
│   │   │         APPROVALS (all must pass):
│   │   │           • DTI < 43%
│   │   │           • Credit ≥ 650
│   │   │           • LTI < 3.0x
│   │   │           • Low employment risk
│   │   │         MANUAL REVIEW:
│   │   │           • DTI 43-50% (near threshold)
│   │   │           • Credit 600-650 (fair range)
│   │   │           • Multiple moderate factors
│   │   │       Risk Calculation:
│   │   │         Components: DTI, Credit, LTI, Income, Employment, Anomalies
│   │   │         Weights: Normalized 0.0-1.0
│   │   │
│   │   └── mock_data.py
│   │       └─ 🎯 Mock Databases
│   │           Provides:
│   │             • Credit history data
│   │             • Employment records
│   │             • Applicant profiles
│   │             • Test scenarios
│   │           Used by: All MCP servers
│   │
├── 🧪 TESTING
│   ├── test_units.py
│   │   └─ 🎯 Unit Tests (9 test cases)
│   │       Tests:
│   │         • Hard rejections (DTI, credit, anomalies)
│   │         • Approval cases
│   │         • Manual review cases
│   │         • Risk score calculations
│   │       Run: python test_units.py
│   │       Status: ✅ All 9 PASS
│   │       Dependencies: None (runs standalone)
│   │
│   ├── test_api.py
│   │   └─ 🎯 Integration Tests
│   │       Tests:
│   │         • End-to-end workflow
│   │         • All services together
│   │         • Response validation
│   │         • Error scenarios
│   │       Run: python test_api.py (after bash run_all.sh)
│   │       Dependencies: All 6 services running
│   │
│   └── test_interactive.py
│       └─ 🎯 Interactive Manual Testing
│           Features:
│             • Manual data entry for all 13 fields
│             • Input validation with feedback
│             • Application summary display
│             • Full result display
│             • Multiple applications support
│           Run: python test_interactive.py
│           Use Case: Manual testing, demonstration
│
├── 🐳 DOCKER & DEPLOYMENT
│   ├── Dockerfile
│   │   └─ 🎯 Container Image Definition
│   │       Base: Python 3.11 slim
│   │       Installs:
│   │         • System dependencies
│   │         • Python packages (requirements.txt)
│   │       Exposes: Ports 8000-8004, 8501
│   │       Default CMD: run_all.sh
│   │
│   ├── docker-compose.yml
│   │   └─ 🎯 Service Orchestration
│   │       Services (6 total):
│   │         1. applicant_db_mcp (Port 8001)
│   │         2. risk_rules_db_mcp (Port 8002)
│   │         3. decision_synthesis_mcp (Port 8003)
│   │         4. notification_system_mcp (Port 8004)
│   │         5. fastapi_service (Port 8000)
│   │         6. streamlit_ui (Port 8501)
│   │       Features:
│   │         • Health checks
│   │         • Dependency ordering
│   │         • Environment variables
│   │         • Network isolation
│   │
│   ├── run_all.sh
│   │   └─ 🎯 Start All Services (1 command)
│   │       Runs:
│   │         1. Activate virtual environment
│   │         2. Create logs directory
│   │         3. Start 4 MCP servers
│   │         4. Start FastAPI service
│   │         5. Start Streamlit UI
│   │         6. Save PIDs for tracking
│   │         7. Auto-open browser
│   │       Time: 3-5 seconds
│   │       Output: Services ready, browser opens
│   │
│   └── stop_all.sh
│       └─ 🎯 Stop All Services
│           Reads PID file and terminates all services
│           Cleans up temporary files
│
├── 📋 CONFIGURATION
│   ├── requirements.txt
│   │   └─ 🎯 Python Dependencies
│   │       Packages:
│   │         • fastapi, uvicorn (REST API)
│   │         • langgraph, langchain (Orchestration)
│   │         • anthropic (Claude API)
│   │         • streamlit (UI)
│   │         • pydantic (Validation)
│   │         • python-dotenv (Environment)
│   │
│   ├── .env.example
│   │   └─ 🎯 Environment Template
│   │       Template for .env file
│   │       Shows required variables
│   │
│   └── .env
│       └─ 🎯 Environment Variables (Not committed)
│           Contains:
│             • ANTHROPIC_API_KEY (required)
│           Security: In .gitignore
│
└── 📚 DOCUMENTATION (15+ files)
    ├── README.md
    │   └─ Main project documentation
    ├── QUICKSTART.md
    │   └─ Quick start guide
    ├── ARCHITECTURE.md
    │   └─ Architecture details
    ├── RUN_TESTS.md
    │   └─ Testing guide
    ├── DEPLOYMENT_QUICK_START.md
    │   └─ Docker deployment reference
    ├── PROJECT_SUMMARY.md
    │   └─ Project overview
    ├── PROJECT_STRUCTURE_GUIDE.md (THIS FILE)
    │   └─ Complete structure explanation
    ├── EVALUATION_REPORT_*.md
    │   └─ Comprehensive evaluation
    └── [Additional documentation files]
```

---

## 📊 Component Interactions Matrix

### Which Files Communicate?

```
Streamlit UI (streamlit_app.py)
    ↓ HTTP POST /apply-loan
FastAPI App (microservices/app.py)
    ↓ calls
LangGraph Workflow (orchestration/workflow.py)
    ├─ imports agents from agents/*.py
    ├─ imports schemas from microservices/schemas.py
    ├─ imports decision_rules from utils/decision_rules.py
    ├─ imports config from utils/config.py
    └─ executes with WorkflowState (orchestration/state.py)

Agents (agents/*.py)
    ├─ call MCP servers via HTTP
    ├─ use schemas from microservices/schemas.py
    ├─ use mock_data from utils/mock_data.py
    └─ use config from utils/config.py

MCP Servers (mcp_servers/*.py)
    ├─ use mock_data from utils/mock_data.py
    ├─ decision_synthesis.py uses decision_rules from utils/
    ├─ all return schemas-compatible JSON
    └─ all run on separate ports (8001-8004)

Tests (test_*.py)
    ├─ test_units.py: imports decision_rules
    ├─ test_api.py: calls http://localhost:8000
    └─ test_interactive.py: calls http://localhost:8000
```

---

## 🔄 Data Flow Diagram

```
┌──────────────────────────────────────────────────────────────┐
│                    USER ACTION                               │
│           Fill form in Streamlit UI (9 fields)               │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────────┐
│              DATA VALIDATION (Pydantic)                      │
│         microservices/schemas.py: LoanApplication            │
│    Type checking, range validation, required fields          │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────────┐
│           API ENDPOINT (/apply-loan)                         │
│         microservices/routes.py → microservices/app.py       │
│              Creates workflow instance                       │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────────┐
│      LANGGRAPH WORKFLOW (orchestration/workflow.py)          │
│           Creates WorkflowState (orchestration/state.py)     │
└────────┬──────────────────────────┬──────────────────────────┘
         │                          │
         ▼ PARALLEL                 ▼ PARALLEL
    ┌─────────────┐          ┌─────────────────┐
    │ Agent 1     │          │ Agent 2         │
    │ (Profile)   │          │ (Financial)     │
    │agents/      │          │agents/          │
    │applicant_   │          │financial_risk_  │
    │agent.py     │          │agent.py         │
    └──────┬──────┘          └────────┬────────┘
           │                          │
           ▼ calls                    ▼ calls
    ┌─────────────┐          ┌─────────────────┐
    │ MCP 1       │          │ MCP 2           │
    │ Port 8001   │          │ Port 8002       │
    │ applicant_  │          │ risk_rules_     │
    │ db.py       │          │ db.py           │
    │             │          │                 │
    │ Returns:    │          │ Returns:        │
    │ Profile     │          │ Financial       │
    │ Result      │          │ Result          │
    └──────┬──────┘          └────────┬────────┘
           │                          │
           └──────────────┬───────────┘
                          │
                   BARRIER: Wait
                          │
                          ▼
         ┌────────────────────────────────┐
         │      Agent 3 (Decision)        │
         │ agents/loan_decision_agent.py  │
         └──────────────┬─────────────────┘
                        │
                        ▼ calls
         ┌────────────────────────────────┐
         │      MCP 3: Decision           │
         │      Port 8003                 │
         │ decision_synthesis.py          │
         │                                │
         │ Applies: decision_rules.py     │
         │ - Hard rejections              │
         │ - Approval criteria            │
         │ - Manual review                │
         │ - Risk score calculation       │
         │                                │
         │ Returns: Decision Result       │
         └──────────────┬─────────────────┘
                        │
                        ▼
         ┌────────────────────────────────┐
         │    Agent 4 (Compliance)        │
         │ agents/compliance_agent.py     │
         └──────────────┬─────────────────┘
                        │
                        ▼ calls
         ┌────────────────────────────────┐
         │   MCP 4: Notification          │
         │   Port 8004                    │
         │ notification_system.py         │
         │                                │
         │ Returns: Compliance Result     │
         └──────────────┬─────────────────┘
                        │
                        ▼
         ┌────────────────────────────────┐
         │   Build Response from State    │
         │ _build_response_from_graph_    │
         │ state() in workflow.py         │
         │                                │
         │ Converts to:                   │
         │ LoanDecisionResponse (schema)  │
         └──────────────┬─────────────────┘
                        │
                        ▼
         ┌────────────────────────────────┐
         │    Return JSON Response        │
         │ FastAPI → Streamlit            │
         │                                │
         │ Contains:                      │
         │ - decision                     │
         │ - risk_score                   │
         │ - confidence                   │
         │ - factors                      │
         │ - explanation                  │
         │ - detailed analysis            │
         └──────────────┬─────────────────┘
                        │
                        ▼
         ┌────────────────────────────────┐
         │    Display Results             │
         │ streamlit_app.py               │
         │                                │
         │ Shows:                         │
         │ - Decision (colored)           │
         │ - Metrics dashboard            │
         │ - Explanation                  │
         │ - Key factors                  │
         │ - Detailed tabs                │
         │ - Application history          │
         └────────────────────────────────┘
```

---

## 🎯 File Purpose Summary Table

| File | Lines | Purpose | Input | Output |
|------|-------|---------|-------|--------|
| applicant_agent.py | ~80 | Profile analysis | LoanApplication | ApplicantProfileResult |
| financial_risk_agent.py | ~90 | Financial risk eval | LoanApplication | FinancialRiskResult |
| loan_decision_agent.py | ~80 | Decision synthesis | App + Results 1&2 | LoanDecisionResult |
| compliance_agent.py | ~70 | Compliance & notify | App + Decision | ComplianceResult |
| applicant_db.py | ~100 | MCP: Applicant data | Query request | Profile data |
| risk_rules_db.py | ~120 | MCP: Risk rules | Financial query | Risk assessment |
| decision_synthesis.py | ~120 | MCP: Decision | Analysis data | Decision + score |
| notification_system.py | ~100 | MCP: Notifications | Decision data | Compliance result |
| workflow.py | ~280 | LangGraph orchestration | - | Calls all agents |
| state.py | ~30 | State definitions | - | Type definitions |
| app.py | ~50 | FastAPI setup | - | Application instance |
| schemas.py | ~70 | Pydantic models | - | Validation schemas |
| routes.py | ~40 | API endpoints | JSON request | JSON response |
| streamlit_app.py | ~215 | UI interface | User input | Decision display |
| decision_rules.py | ~255 | Business rules | Metrics | Decision & score |
| mock_data.py | ~150 | Test data | - | Mock records |
| config.py | ~40 | Configuration | .env file | Config object |
| test_units.py | ~150 | Unit tests | - | Test results |
| test_api.py | ~100 | Integration tests | - | Test results |
| test_interactive.py | ~335 | Interactive tests | User input | Results |

---

## 🚀 Quick Reference: Which File to Modify?

| Need | File(s) to Modify |
|------|------------------|
| Change decision logic | `utils/decision_rules.py` |
| Add new form field | `ui/streamlit_app.py` + `microservices/schemas.py` |
| Modify agent behavior | `agents/applicant_agent.py` (or relevant) |
| Change API response | `microservices/schemas.py` + `microservices/routes.py` |
| Add new API endpoint | `microservices/routes.py` |
| Change MCP server behavior | `mcp_servers/*.py` |
| Update mock data | `utils/mock_data.py` |
| Change UI appearance | `ui/streamlit_app.py` |
| Fix configuration | `utils/config.py` or `.env` |
| Add new test case | `test_units.py` or `test_api.py` |
| Change deployment | `Dockerfile`, `docker-compose.yml`, `run_all.sh` |

---

## 📈 Complexity Metrics

| Aspect | Complexity |
|--------|-----------|
| **Number of Files** | 30+ |
| **Total Lines of Code** | ~2500+ |
| **Number of APIs** | 2 (REST) + 8+ (MCP) |
| **Database Tables** | 0 (mock data) |
| **External Dependencies** | Anthropic API (required) |
| **Services Running** | 6 |
| **Ports Used** | 5 (8000-8004, 8501) |
| **Test Coverage** | 9 unit tests |
| **Documentation Files** | 15+ |

---

**Created**: 2026-06-22  
**For**: Understanding complete project structure
