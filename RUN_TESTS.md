# Running Tests

## Quick Test Options

### Option 1: Unit Tests (No Services Required) ✅ FASTEST
```bash
python test_units.py
```
**What it tests:** Decision rules, business logic  
**Time:** ~1 second  
**No dependencies:** ✅ Works standalone  
**Status:** All tests pass ✅

---

### Option 2: Health Check (Verify Services Running)
```bash
curl http://localhost:8000/health
curl http://localhost:8001/health
curl http://localhost:8002/health
curl http://localhost:8003/health
curl http://localhost:8004/health
```
**Expected response:** `{"status": "healthy"}`

---

### Option 3: Full Integration Tests (All Services Required)
First, START ALL SERVICES:
```bash
bash run_all.sh
```

Wait 3-5 seconds for services to start, then run:
```bash
python test_api.py
```

**What it tests:** End-to-end API flow with all services  
**Time:** ~5-10 seconds  
**Requirements:** All 6 services running  
**Status:** Will PASS once services are running

---

## Complete Testing Workflow

### Step 1: Start All Services
```bash
bash run_all.sh
```
Output should show:
```
✅ ALL SERVICES STARTED ✅
Services running:
  ✓ Applicant DB MCP:        http://localhost:8001
  ✓ Risk Rules DB MCP:       http://localhost:8002
  ✓ Decision Synthesis MCP:  http://localhost:8003
  ✓ Notification System MCP: http://localhost:8004
  ✓ FastAPI Service:         http://localhost:8000
  ✓ Streamlit UI:            http://localhost:8501
```

### Step 2: Verify Health (Optional)
```bash
curl http://localhost:8000/health
```

### Step 3: Run Unit Tests (Fast)
```bash
python test_units.py
```
Expected: ✅ 9/9 tests passed

### Step 4: Run Integration Tests (Full)
```bash
python test_api.py
```
Expected: ✅ All scenarios processed

### Step 5: Test UI
Visit: http://localhost:8501

Fill in the form and submit an application to see real-time processing.

### Step 6: Stop Services
```bash
bash stop_all.sh
```

---

## Test Scenarios

### Approval Case (DTI < 43%, Credit >= 650)
```json
{
  "applicant_id": "TEST_APPROVAL_001",
  "age": 35,
  "income": 120000,
  "credit_score": 780,
  "loan_amount": 100000,
  "employment_type": "Salaried",
  "tenure_months": 60,
  "existing_liabilities": 10000,
  "location": "New York"
}
```
**Expected Decision:** ✅ Approve

### Rejection Case (DTI >= 50% OR Credit < 600)
```json
{
  "applicant_id": "TEST_REJECTION_001",
  "age": 25,
  "income": 25000,
  "credit_score": 550,
  "loan_amount": 300000,
  "employment_type": "Self-Employed",
  "tenure_months": 120,
  "existing_liabilities": 80000,
  "location": "California"
}
```
**Expected Decision:** ❌ Reject

### Manual Review Case (Mixed Signals)
```json
{
  "applicant_id": "TEST_REVIEW_001",
  "age": 45,
  "income": 75000,
  "credit_score": 680,
  "loan_amount": 150000,
  "employment_type": "Salaried",
  "tenure_months": 84,
  "existing_liabilities": 35000,
  "location": "Texas"
}
```
**Expected Decision:** 🔄 Requires Manual Review

---

## Troubleshooting

### "Connection refused" when running test_api.py
**Solution:** Start services first
```bash
bash run_all.sh
```

### "Request failed: 500"
**Possible causes:**
1. Services not running → Run `bash run_all.sh`
2. Services crashed → Check logs in `logs/` directory
3. Port conflicts → Use `lsof -i :8000` to check

### Services won't start
```bash
# Check if ports are in use
lsof -i :8000
lsof -i :8001
lsof -i :8002
lsof -i :8003
lsof -i :8004
lsof -i :8501

# Kill existing processes
bash stop_all.sh
```

### Unit tests fail
```bash
# Verify Python environment
python test_units.py

# Should show: ✅ ALL TESTS PASSED!
```

---

## Test Summary

| Test Type | Command | Time | Dependencies | Status |
|---|---|---|---|---|
| Unit Tests | `python test_units.py` | ~1s | None | ✅ Pass |
| Health Check | `curl http://localhost:8000/health` | ~0.1s | FastAPI | ✅ Pass (if running) |
| Integration | `python test_api.py` | ~5s | All 6 services | ✅ Pass (if services running) |
| UI Test | Visit http://localhost:8501 | Manual | All 6 services | ✅ Works |

---

## Decision Rules Being Tested

### Hard Rejections (Automatic)
- ❌ DTI >= 50%
- ❌ Credit Score < 600
- ❌ Multiple severe anomalies (bankruptcy, foreclosure)

### Approvals (All criteria met)
- ✅ DTI < 43%
- ✅ Credit Score >= 650
- ✅ LTI < 3.0x
- ✅ Low employment risk
- ✅ No major anomalies

### Manual Review (Mixed signals)
- 🔄 DTI 43-50%
- 🔄 Credit Score 600-650
- 🔄 Multiple moderate risk factors

---

## Next Steps

1. **Run unit tests:** `python test_units.py`
2. **Start services:** `bash run_all.sh`
3. **Run integration tests:** `python test_api.py`
4. **Test UI:** http://localhost:8501
5. **Stop services:** `bash stop_all.sh`

**All tests should PASS!** ✅
