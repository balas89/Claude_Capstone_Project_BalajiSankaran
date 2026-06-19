# System Architecture & Design

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                           │
│                  Streamlit Web Interface                         │
│              (http://localhost:8501)                             │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               │ HTTP Requests
                               ↓
┌─────────────────────────────────────────────────────────────────┐
│                   MICROSERVICES LAYER                            │
│              FastAPI REST API Orchestrator                       │
│              (http://localhost:8000)                             │
│                 POST /apply-loan endpoint                        │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                   ┌───────────┴───────────┐
                   │                       │
                   ↓                       ↓
        ┌──────────────────────────────────────────────────┐
        │      ORCHESTRATION LAYER (LangGraph)             │
        │   - State Management                             │
        │   - Workflow Coordination                        │
        │   - Error Handling                               │
        └──────────────────────────────────────────────────┘
                   │
        ┌──────────┼──────────┬──────────┬──────────┐
        │          │          │          │          │
        ↓          ↓          ↓          ↓          ↓
   ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐
   │  Agent 1   │ │  Agent 2   │ │  Agent 3   │ │  Agent 4   │
   │ Applicant  │ │ Financial  │ │Loan        │ │Compliance  │
   │ Profile    │ │ Risk       │ │Decision    │ │ &Action    │
   └──────┬─────┘ └──────┬─────┘ └──────┬─────┘ └──────┬─────┘
          │              │              │              │
          │              │              │              │
   ┌──────↓──────┐ ┌─────↓──────┐ ┌────↓───────┐ ┌────↓───────┐
   │   MCP 8001  │ │  MCP 8002  │ │  MCP 8003  │ │  MCP 8004  │
   │ ApplicantDB │ │RiskRulesDB │ │ Decision   │ │Notification│
   │             │ │            │ │Synthesis   │ │ System     │
   └──────┬──────┘ └──────┬─────┘ └──────┬─────┘ └──────┬─────┘
          │              │              │              │
          ↓              ↓              ↓              ↓
   ┌──────────────────────────────────────────────────────────┐
   │              DATA & EXTERNAL SERVICES LAYER              │
   │                                                          │
   │  • Mock Credit History DB                                │
   │  • Mock Employment Verification                          │
   │  • Mock Compliance Rules Engine                          │
   │  • Claude LLM API (for decision synthesis)               │
   │  • Mock Audit Trail & Notifications                      │
   └──────────────────────────────────────────────────────────┘
```

## Component Details

### Layer 1: Presentation Layer
**Technology**: Streamlit
- Interactive form-based UI
- Real-time decision display
- Detailed analysis tabs
- Application history
- Decision explanations

**Files**:
- `ui/streamlit_app.py`

---

### Layer 2: Microservices Layer
**Technology**: FastAPI
- RESTful API endpoints
- Request validation (Pydantic)
- CORS support
- Health check endpoint
- Automatic documentation (Swagger UI)

**Endpoints**:
```
POST /apply-loan          → Process loan application
GET  /health             → Health check
GET  /docs               → Swagger UI
GET  /redoc              → ReDoc documentation
```

**Files**:
- `microservices/app.py`
- `microservices/routes.py`
- `microservices/schemas.py` (Pydantic models)

---

### Layer 3: Orchestration Layer
**Technology**: LangGraph (Graph-based workflow engine)

**Workflow Steps**:
1. Initialize application state
2. Execute Applicant Profile Agent
3. Execute Financial Risk Agent
4. Execute Loan Decision Agent (with Claude)
5. Execute Compliance Agent
6. Return final decision

**Error Handling**:
- Try-catch blocks at each step
- Error logging to state
- Graceful fallbacks
- Comprehensive error messages

**Files**:
- `orchestration/workflow.py` (Main workflow)
- `orchestration/state.py` (State management)

---

### Layer 4: Agent Layer

#### Agent 1: Applicant Profile Agent
**Responsibility**: Analyze applicant demographics and creditworthiness
**Input**:
- Applicant ID, Age, Income, Employment Type, Credit Score

**Processing**:
1. Query credit history database
2. Verify employment status
3. Calculate income stability score (0-1)
4. Determine employment risk level
5. Identify completeness flags

**Output**:
```json
{
  "income_stability_score": 0.75,
  "employment_risk": "Low",
  "credit_history_summary": { ... },
  "completeness_flags": [ ... ]
}
```

**File**: `agents/applicant_agent.py`

---

#### Agent 2: Financial Risk Agent
**Responsibility**: Evaluate financial risk metrics
**Input**:
- Income, Credit Score, Loan Amount, Tenure, Existing Liabilities

**Processing**:
1. Calculate monthly income and obligations
2. Compute debt-to-income ratio
3. Assess credit risk level
4. Evaluate loan amount risk
5. Detect anomalies

**Output**:
```json
{
  "dti_ratio": 0.38,
  "credit_risk_level": "Low",
  "loan_amount_risk": "Medium",
  "anomalies": [ ... ],
  "reasoning": "..."
}
```

**File**: `agents/financial_risk_agent.py`

---

#### Agent 3: Loan Decision Agent (LLM-Powered)
**Responsibility**: Synthesize final decision using Claude
**Input**:
- Profile analysis results
- Financial analysis results
- Loan details

**Processing**:
1. Format comprehensive prompt with all analyses
2. Call Claude Sonnet via MCP DecisionSynthesis
3. Parse Claude's JSON response
4. Return structured decision

**Output**:
```json
{
  "decision": "Approve|Reject|Requires Manual Review",
  "risk_score": 0.3,
  "confidence": 0.85,
  "key_factors": [ ... ],
  "explanation": "..."
}
```

**File**: `agents/loan_decision_agent.py`

---

#### Agent 4: Compliance & Action Orchestrator Agent
**Responsibility**: Execute compliance checks and take actions
**Input**:
- Application data
- Decision result
- All analysis results

**Processing**:
1. Run compliance checks
2. Log decision to audit trail
3. Send notifications
4. Generate case ID
5. Create summary

**Output**:
```json
{
  "action_taken": "...",
  "notification_sent": true,
  "case_id": "CASE_APP001_...",
  "timestamp": "2024-01-15T10:30:00",
  "summary": "..."
}
```

**File**: `agents/compliance_agent.py`

---

### Layer 5: MCP Server Layer
**Technology**: FastAPI + Model Context Protocol

#### MCP Server 1: ApplicantDB (Port 8001)
**Purpose**: Applicant profile analysis
**Endpoints**:
- `GET /health` → Service status
- `POST /get_applicant_profile` → Get profile analysis

**Data Sources**:
- Mock credit history
- Mock employment verification

**File**: `mcp_servers/applicant_db.py`

---

#### MCP Server 2: RiskRulesDB (Port 8002)
**Purpose**: Financial risk analysis
**Endpoints**:
- `GET /health` → Service status
- `POST /analyze_financial_risk` → Get risk analysis

**Rules**:
- DTI threshold: 0.43 (recommended), 0.50 (critical)
- Credit score: 750 (Low), 650 (Medium), 600 (High)
- Loan thresholds: 5x income (Medium), 2x income (Low)

**File**: `mcp_servers/risk_rules_db.py`

---

#### MCP Server 3: DecisionSynthesis (Port 8003)
**Purpose**: LLM-based decision synthesis
**Endpoints**:
- `GET /health` → Service status
- `POST /synthesize_decision` → Get Claude decision

**LLM Integration**:
- Model: Claude Sonnet 4.6
- API: Anthropic SDK
- Context: Complete analysis summary

**File**: `mcp_servers/decision_synthesis.py`

---

#### MCP Server 4: NotificationSystem (Port 8004)
**Purpose**: Compliance & notifications
**Endpoints**:
- `GET /health` → Service status
- `POST /execute_compliance_and_notify` → Execute compliance
- `GET /audit_trail` → Retrieve audit trail
- `GET /notifications` → Retrieve notifications

**Features**:
- Compliance verification
- Audit logging
- Notification sending
- Case tracking

**File**: `mcp_servers/notification_system.py`

---

### Layer 6: Data Layer

#### Mock Databases
- **Credit History**: Simulates real credit bureau data
- **Employment Verification**: Simulates employment validation
- **Compliance Rules**: Simulates regulatory requirements
- **Audit Trail**: Logs all decisions
- **Notifications**: Tracks sent notifications

**File**: `utils/mock_data.py`

---

## Data Flow Diagram

```
┌──────────────────────────────────────────────────────────┐
│  User fills form in Streamlit UI                         │
│  Applicant ID, Age, Income, Employment, Credit Score,    │
│  Loan Amount, Tenure, Liabilities, Location              │
└────────────────────────┬─────────────────────────────────┘
                         │
                         ↓
┌──────────────────────────────────────────────────────────┐
│  POST /apply-loan (FastAPI)                              │
│  Request validation via Pydantic LoanApplication schema   │
└────────────────────────┬─────────────────────────────────┘
                         │
                         ↓
┌──────────────────────────────────────────────────────────┐
│  LangGraph Orchestration Engine                          │
│  Initialize ApplicationState                             │
└────────────────────────┬─────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        ↓                ↓                ↓
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│Agent 1 →8001 │ │Agent 2 →8002 │ │Agent 3 →8003 │
│Profile Data  │ │Financial Risk│ │Claude        │
└──────────────┘ └──────────────┘ │Decision      │
        │                │        └──────────────┘
        │                │              │
        └────────────────┼──────────────┘
                         │
                         ↓
        ┌────────────────────────────────┐
        │ Synthesize Results             │
        │ Build comprehensive state      │
        └────────────────┬───────────────┘
                         │
                         ↓
┌──────────────────────────────────────────────────────────┐
│  Agent 4 → 8004                                          │
│  Compliance Check & Notifications                        │
│  Log to Audit Trail                                      │
└────────────────────────┬─────────────────────────────────┘
                         │
                         ↓
┌──────────────────────────────────────────────────────────┐
│  LoanDecisionResponse                                    │
│  {                                                       │
│    case_id, applicant_id, decision, risk_score,         │
│    confidence, factors, explanation,                    │
│    profile_analysis, financial_analysis,                │
│    compliance_status, timestamp                         │
│  }                                                       │
└────────────────────────┬─────────────────────────────────┘
                         │
                         ↓
┌──────────────────────────────────────────────────────────┐
│  Streamlit UI displays decision                          │
│  Shows metrics, factors, and detailed analysis           │
└──────────────────────────────────────────────────────────┘
```

## Decision Logic

### Credit Risk Level
```
Credit Score ≥ 750        → Low
650 ≤ Credit Score < 750  → Medium
600 ≤ Credit Score < 650  → High
Credit Score < 600        → Critical
```

### Employment Risk
```
Employment Not Verified        → High
Job Stability Score < 0.5      → Medium
Job Stability Score ≥ 0.5      → Low
```

### Loan Amount Risk
```
Loan > 10x Income              → Excessive
5x Income < Loan ≤ 10x Income  → High
2x Income < Loan ≤ 5x Income   → Medium
Loan ≤ 2x Income               → Low
```

### DTI (Debt-to-Income) Risk
```
DTI > 0.50                 → Critical (will flag for review)
0.43 < DTI ≤ 0.50         → Above recommended (caution)
DTI ≤ 0.43                → Acceptable
```

### Anomalies Detected
- Income below minimum threshold ($20,000)
- DTI ratio critically high (>0.50)
- Credit score in poor range
- Loan amount significantly exceeds income
- Loan tenure too short (<12 months)
- Loan tenure excessive (>360 months)

## Security Considerations

1. **API Authentication**: Add JWT/OAuth in production
2. **Rate Limiting**: Implement to prevent abuse
3. **Encryption**: Use HTTPS/TLS for all communications
4. **Secrets Management**: Use secure vaults for API keys
5. **Input Validation**: Comprehensive validation already implemented
6. **Logging**: Audit trails for compliance
7. **Error Handling**: Non-exposing error messages

## Scalability Considerations

1. **Horizontal Scaling**: Each MCP server can scale independently
2. **Load Balancing**: Can distribute API requests across instances
3. **Database**: Replace mock DBs with real scalable databases
4. **Caching**: Implement Redis for credit history caching
5. **Async Processing**: Current system already uses async/await
6. **Message Queue**: Can add Kafka for high-volume processing

## Monitoring & Observability

**Metrics to Track**:
- Decision approval rate
- Average processing time
- Error rate by component
- API response times
- MCP server availability

**Logs**:
- Application logs
- Agent processing logs
- MCP server logs
- Decision audit trail

**Alerts**:
- MCP server down
- High error rate
- Slow processing times
- API failures
