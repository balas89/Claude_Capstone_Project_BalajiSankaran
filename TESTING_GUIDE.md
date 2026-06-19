# Comprehensive Testing Guide

## Pre-Testing Checklist

- [ ] ANTHROPIC_API_KEY environment variable is set
- [ ] Python 3.8+ installed
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] All required ports (8000-8004, 8501) are available
- [ ] No previous processes running on these ports

## Testing Levels

---

## Level 1: Individual Component Testing

### 1.1 Testing MCP Server - ApplicantDB (Port 8001)

**Start the server**:
```bash
python3 -m mcp_servers.applicant_db
```

**Test endpoint**:
```bash
curl -X POST http://localhost:8001/get_applicant_profile \
  -H "Content-Type: application/json" \
  -d '{
    "applicant_id": "TEST_001",
    "age": 35,
    "income": 80000,
    "employment_type": "Salaried",
    "credit_score": 720
  }'
```

**Expected Response**:
```json
{
  "applicant_id": "TEST_001",
  "income_stability_score": 0.75,
  "employment_risk": "Low",
  "credit_history_summary": {
    "credit_score": 720,
    "payment_history": "Good",
    "accounts_count": 8,
    "late_payments_6m": 0,
    "late_payments_12m": 1,
    "collections": 0,
    "inquiries_6m": 2
  },
  "employment_verified": true,
  "years_employed": 8,
  "completeness_flags": []
}
```

---

### 1.2 Testing MCP Server - RiskRulesDB (Port 8002)

**Start the server**:
```bash
python3 -m mcp_servers.risk_rules_db
```

**Test endpoint**:
```bash
curl -X POST http://localhost:8002/analyze_financial_risk \
  -H "Content-Type: application/json" \
  -d '{
    "applicant_id": "TEST_001",
    "income": 80000,
    "credit_score": 720,
    "loan_amount": 100000,
    "tenure_months": 60,
    "existing_liabilities": 15000
  }'
```

**Expected Response**:
```json
{
  "applicant_id": "TEST_001",
  "dti_ratio": 0.240,
  "credit_risk_level": "Low",
  "loan_amount_risk": "Medium",
  "anomalies": [],
  "reasoning": "DTI: 0.24, Credit Risk: Low, Loan Risk: Medium, Anomalies: 0",
  "monthly_income": 6666.67,
  "monthly_obligations": 1600.0
}
```

---

### 1.3 Testing MCP Server - DecisionSynthesis (Port 8003)

**Start the server**:
```bash
python3 -m mcp_servers.decision_synthesis
# Requires ANTHROPIC_API_KEY to be set
```

**Test endpoint**:
```bash
curl -X POST http://localhost:8003/synthesize_decision \
  -H "Content-Type: application/json" \
  -d '{
    "applicant_id": "TEST_001",
    "profile_analysis": {
      "income_stability_score": 0.75,
      "employment_risk": "Low",
      "credit_history_summary": {
        "credit_score": 720,
        "payment_history": "Good"
      },
      "completeness_flags": []
    },
    "financial_analysis": {
      "dti_ratio": 0.24,
      "credit_risk_level": "Low",
      "loan_amount_risk": "Medium",
      "anomalies": []
    },
    "loan_details": {
      "loan_amount": 100000,
      "tenure_months": 60,
      "income": 80000,
      "existing_liabilities": 15000
    }
  }'
```

**Expected Response**:
```json
{
  "applicant_id": "TEST_001",
  "decision": "Approve",
  "confidence": 0.85,
  "risk_score": 0.25,
  "key_factors": [
    "Good credit score (720)",
    "Stable employment",
    "Healthy DTI ratio",
    "Reasonable loan amount"
  ],
  "explanation": "Applicant demonstrates strong financial profile with good credit history, stable employment, and healthy debt-to-income ratio. Loan amount is reasonable relative to income."
}
```

---

### 1.4 Testing MCP Server - NotificationSystem (Port 8004)

**Start the server**:
```bash
python3 -m mcp_servers.notification_system
```

**Test endpoint**:
```bash
curl -X POST http://localhost:8004/execute_compliance_and_notify \
  -H "Content-Type: application/json" \
  -d '{
    "applicant_id": "TEST_001",
    "location": "New York",
    "decision": "Approve",
    "risk_factors": {
      "risk_score": 0.25,
      "dti_ratio": 0.24,
      "credit_risk": "Low"
    },
    "profile_analysis": {}
  }'
```

**Expected Response**:
```json
{
  "applicant_id": "TEST_001",
  "action_taken": "Decision Approve - Notification sent",
  "notification_sent": true,
  "case_id": "CASE_TEST_001_20240115101500",
  "timestamp": "2024-01-15T10:15:00.123456",
  "summary": "Application CASE_TEST_001_20240115101500 processed with decision: Approve"
}
```

---

## Level 2: Service Integration Testing

### 2.1 Test FastAPI Microservice

**Start all MCP servers first** (as shown above in parallel)

**Start FastAPI**:
```bash
python3 -m microservices.app
```

**Health check**:
```bash
curl http://localhost:8000/health
```

**Expected Response**:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:15:00.123456"
}
```

**Full loan application test**:
```bash
curl -X POST http://localhost:8000/apply-loan \
  -H "Content-Type: application/json" \
  -d '{
    "applicant_id": "INTEGRATION_TEST_001",
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

**Expected Response**:
```json
{
  "case_id": "CASE_INTEGRATION_TEST_001_20240115101500",
  "applicant_id": "INTEGRATION_TEST_001",
  "decision": "Approve",
  "risk_score": 0.25,
  "confidence": 0.85,
  "factors": [
    "Good credit score",
    "Stable employment",
    "Healthy DTI ratio"
  ],
  "explanation": "...",
  "profile_analysis": { ... },
  "financial_analysis": { ... },
  "compliance_status": { ... },
  "timestamp": "2024-01-15T10:15:00.123456"
}
```

---

## Level 3: End-to-End Testing

### 3.1 Using Python Test Script

**Prepare**:
1. Start all services (MCP servers + FastAPI)
2. Ensure ANTHROPIC_API_KEY is set

**Run tests**:
```bash
python3 test_api.py
```

**Expected Output**:
```
════════════════════════════════════════════════════════
  LOAN APPROVAL SYSTEM - API TEST SUITE
════════════════════════════════════════════════════════

Testing Health Check Endpoint
✅ Health check passed

Testing Loan Application: approval_case
Input: {...}
✅ Application processed successfully
Decision: Approve
Risk Score: 25.00%
Confidence: 85.00%
Case ID: CASE_TEST_APPROVAL_001_...

Testing Loan Application: rejection_case
✅ Application processed successfully
Decision: Reject
Risk Score: 85.00%
Confidence: 90.00%
Case ID: CASE_TEST_REJECTION_001_...

TEST SUMMARY
✅ approval_case: Approve
✅ rejection_case: Reject
✅ review_case: Requires Manual Review
```

---

### 3.2 Using Streamlit UI

**Prepare**:
1. Start all services
2. Start Streamlit: `streamlit run ui/streamlit_app.py`

**Manual Test Steps**:

1. **Navigate to UI**: Open http://localhost:8501

2. **Fill Application Form**:
   - Applicant ID: `STREAMLIT_TEST_001`
   - Age: 35
   - Income: $100,000
   - Employment: Salaried
   - Credit Score: 750
   - Loan Amount: $80,000
   - Tenure: 60 months
   - Liabilities: $5,000
   - Location: New York

3. **Submit Application**:
   - Click "Submit Application" button
   - Wait for processing (5-15 seconds)

4. **Verify Results**:
   - Check decision is displayed (✅ APPROVED)
   - Verify Risk Score shows ~25%
   - Confirm Confidence ~85%
   - Review explanation text
   - Check Key Decision Factors list

5. **Check Tabs**:
   - **Profile Analysis**: See income stability, employment risk
   - **Financial Analysis**: View DTI ratio, credit risk level
   - **Compliance**: Verify compliance status
   - **Full Details**: Review complete JSON response

6. **Test Application History**:
   - Application should appear in "Application History" section
   - History should persist during session

---

## Level 4: Performance & Stress Testing

### 4.1 Latency Testing

**Sequential requests**:
```bash
time python3 test_api.py
```

**Expected Performance**:
- First request: 5-15 seconds (Claude API latency)
- Subsequent requests: 2-5 seconds each
- Total for 3 test cases: 15-30 seconds

### 4.2 Concurrent Request Testing

**Using Apache Bench**:
```bash
ab -n 10 -c 3 -p test_payload.json \
   -H "Content-Type: application/json" \
   http://localhost:8000/apply-loan
```

**Where `test_payload.json` contains**:
```json
{
  "applicant_id": "CONCURRENT_001",
  "age": 35,
  "income": 100000,
  "employment_type": "Salaried",
  "credit_score": 750,
  "loan_amount": 80000,
  "tenure_months": 60,
  "existing_liabilities": 5000,
  "location": "New York"
}
```

---

## Level 5: Test Scenarios

### Test Scenario 1: Likely Approval

**Input**:
```json
{
  "applicant_id": "APPROVE_001",
  "age": 40,
  "income": 150000,
  "employment_type": "Salaried",
  "credit_score": 800,
  "loan_amount": 100000,
  "tenure_months": 60,
  "existing_liabilities": 10000,
  "location": "New York"
}
```

**Expected Decision**: ✅ APPROVE
**Expected Risk Score**: 0.15 - 0.25
**Expected Confidence**: > 0.80

---

### Test Scenario 2: Likely Rejection

**Input**:
```json
{
  "applicant_id": "REJECT_001",
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

**Expected Decision**: ❌ REJECT
**Expected Risk Score**: 0.75 - 0.95
**Expected Confidence**: > 0.80

---

### Test Scenario 3: Manual Review Required

**Input**:
```json
{
  "applicant_id": "REVIEW_001",
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

**Expected Decision**: ⚠️ REQUIRES MANUAL REVIEW
**Expected Risk Score**: 0.40 - 0.60
**Expected Confidence**: 0.50 - 0.75

---

### Test Scenario 4: Edge Case - Young Age

**Input**:
```json
{
  "applicant_id": "EDGE_YOUNG",
  "age": 21,
  "income": 45000,
  "employment_type": "Salaried",
  "credit_score": 700,
  "loan_amount": 50000,
  "tenure_months": 48,
  "existing_liabilities": 10000,
  "location": "Florida"
}
```

**Expected**: Completion flag for "Applicant under 21"

---

### Test Scenario 5: Edge Case - Low Income

**Input**:
```json
{
  "applicant_id": "EDGE_LOW_INCOME",
  "age": 35,
  "income": 15000,
  "employment_type": "Salaried",
  "credit_score": 750,
  "loan_amount": 50000,
  "tenure_months": 60,
  "existing_liabilities": 5000,
  "location": "California"
}
```

**Expected**: Anomaly "Income below minimum threshold"

---

## Troubleshooting During Testing

| Issue | Cause | Solution |
|-------|-------|----------|
| "Connection refused" | MCP server not running | Ensure all 4 servers started on ports 8001-8004 |
| "Timeout" | Claude API slow/blocked | Check ANTHROPIC_API_KEY, verify API access |
| "Port already in use" | Process still running | `lsof -ti:8000 \| xargs kill -9` |
| "ModuleNotFoundError" | Dependencies not installed | Run `pip install -r requirements.txt` |
| "Invalid JSON response" | API error | Check MCP server logs |
| "No response from Streamlit" | Port 8501 busy | Change STREAMLIT_SERVER_PORT in .env |

---

## Verification Checklist

After all tests pass:

- [ ] All 4 MCP servers start without errors
- [ ] FastAPI starts and responds to health check
- [ ] Streamlit UI loads without errors
- [ ] Test script completes all 3 scenarios
- [ ] Decision responses include all required fields
- [ ] Approval/rejection scenarios work correctly
- [ ] Audit trail logs decisions
- [ ] Application history displays in Streamlit
- [ ] Performance is acceptable (< 20s per request)
- [ ] Error handling works gracefully
- [ ] UI displays all analysis tabs correctly

---

## Log Analysis

### Where to Find Logs

**MCP Servers**: Console output when running
**FastAPI**: Console output with request timing
**Streamlit**: Browser console + terminal output

### Key Log Patterns to Look For

✅ **Success**:
```
[8001] Processing get_applicant_profile
[8002] Analyzing financial risk
[8003] Synthesizing decision with Claude
[8004] Compliance check passed
```

❌ **Errors**:
```
ConnectionError: Cannot connect to MCP server
TimeoutError: API request timed out
ValidationError: Invalid input format
```

---

## Success Criteria

The system is working correctly when:

1. ✅ All MCP servers respond to health checks
2. ✅ FastAPI accepts loan applications
3. ✅ Claude API is called and returns decisions
4. ✅ Decisions are consistent with input factors
5. ✅ All 4 agents complete without errors
6. ✅ Streamlit UI displays decisions clearly
7. ✅ Audit trail records all applications
8. ✅ Processing time is < 20 seconds
9. ✅ Test scenarios produce expected results
10. ✅ No critical errors in logs
