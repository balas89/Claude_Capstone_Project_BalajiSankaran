# 🚀 Multi-Agent Loan Approval System - Quick Deployment Guide

## The Single Command to Run Everything

```bash
docker-compose up --build
```

That's it! ✅

---

## What Happens When You Run This Command

1. **Builds Docker Images** - Creates optimized images for all services
2. **Starts 6 Containerized Services:**
   - ✅ Applicant DB MCP Server (Port 8001)
   - ✅ Risk Rules DB MCP Server (Port 8002)
   - ✅ Decision Synthesis MCP Server (Port 8003)
   - ✅ Notification System MCP Server (Port 8004)
   - ✅ FastAPI Microservice (Port 8000)
   - ✅ Streamlit Web UI (Port 8501)

3. **Configures Networking** - All services communicate via dedicated Docker network
4. **Enables Health Checks** - Monitors container health automatically
5. **Sets Up Dependencies** - Services start in correct order

---

## Access the System

Once `docker-compose up --build` completes (wait for "Streamlit app is now running"):

### User Interface
- **Streamlit Chatbot UI:** http://localhost:8501
  - Submit loan applications
  - View real-time decisions
  - Analyze decision factors

### API Endpoints (for testing/integration)
- **FastAPI Main Endpoint:** http://localhost:8000
- **Swagger API Docs:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

### MCP Servers (for troubleshooting)
- **Applicant DB:** http://localhost:8001/docs
- **Risk Rules:** http://localhost:8002/docs
- **Decision Synthesis:** http://localhost:8003/docs
- **Notifications:** http://localhost:8004/docs

---

## Prerequisites

### Required
- Docker installed: [Download Docker Desktop](https://www.docker.com/products/docker-desktop)
- Docker Compose: Included with Docker Desktop
- API Key: `ANTHROPIC_API_KEY` set in `.env` file

### Setup

1. **Create .env file** (if not present):
   ```bash
   cp .env.example .env
   ```

2. **Add your Anthropic API Key:**
   ```bash
   # Edit .env and add:
   ANTHROPIC_API_KEY=sk-your-actual-api-key-here
   ```

3. **Run the single command:**
   ```bash
   docker-compose up --build
   ```

---

## Sample Loan Application (for Testing)

Once the UI loads at http://localhost:8501, try these test cases:

### Test Case 1: Likely Approval
```
Applicant ID: APP001
Name: Sarah Johnson
Email: sarah@example.com
Income: $120,000
Employment Years: 8
Credit Score: 750
Loan Amount: $300,000
Employment Type: Full-time
Credit History: Excellent
```
**Expected Decision:** ✅ Approve

### Test Case 2: Likely Rejection
```
Applicant ID: APP002
Name: James Smith
Email: james@example.com
Income: $35,000
Employment Years: 1
Credit Score: 580
Loan Amount: $450,000
Employment Type: Part-time
Credit History: Poor
```
**Expected Decision:** ❌ Reject

### Test Case 3: Manual Review
```
Applicant ID: APP003
Name: Emma Davis
Email: emma@example.com
Income: $85,000
Employment Years: 2
Credit Score: 680
Loan Amount: $350,000
Employment Type: Full-time
Credit History: Fair
```
**Expected Decision:** 🔄 Requires Manual Review

---

## Common Tasks

### View All Logs
```bash
docker-compose logs -f
```

### View Specific Service Logs
```bash
docker-compose logs -f streamlit-ui
docker-compose logs -f fastapi-service
docker-compose logs -f decision-synthesis
```

### Stop All Services
```bash
docker-compose down
```

### Restart a Service
```bash
docker-compose restart fastapi-service
```

### Run Tests Inside Container
```bash
docker-compose exec fastapi-service python test_api.py
```

### Check Service Health
```bash
docker-compose ps
```

---

## Troubleshooting

### "Port already in use"
Edit `docker-compose.yml` and change port mappings:
```yaml
ports:
  - "9000:8000"  # Maps to different host port
```

### "ANTHROPIC_API_KEY not set"
```bash
# Verify .env exists
cat .env

# Or set inline
ANTHROPIC_API_KEY=sk-xxx docker-compose up --build
```

### "Services not starting"
```bash
# Check logs
docker-compose logs

# Rebuild without cache
docker-compose build --no-cache
docker-compose up
```

### "Connection refused"
Wait 10-15 seconds for all services to initialize. Check health:
```bash
docker-compose ps
```

All services should show "healthy" status.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────┐
│  Your Browser                                   │
│  http://localhost:8501 (Streamlit UI)          │
└──────────────┬──────────────────────────────────┘
               │
        ┌──────▼──────┐
        │  Streamlit  │
        │ Container   │
        └──────┬──────┘
               │
        ┌──────▼──────────────┐
        │  FastAPI Container  │
        │  (http://0.0.0.0:8000)
        └──────┬──────────────┘
               │
    ┌──────────┼──────────┐
    │          │          │
 ┌──▼──┐  ┌───▼────┐  ┌──▼───┐
 │ App │  │ Risk   │  │ Decis │
 │ DB  │  │ Rules  │  │ Synth │
 │8001 │  │ 8002   │  │ 8003  │
 └─────┘  └────────┘  └───────┘
    │          │          │
    └──────────┼──────────┘
               │
          ┌────▼────┐
          │ Notif   │
          │ System  │
          │  8004   │
          └─────────┘
```

All services run in Docker containers with automatic networking.

---

## File Structure

```
/project
├── Dockerfile                      ← Container image definition
├── docker-compose.yml              ← Orchestration config
├── .dockerignore                   ← Excluded files
├── DOCKER_DEPLOYMENT.md            ← Detailed Docker guide
├── DEPLOYMENT_QUICK_START.md       ← This file
│
├── mcp_servers/                    ← Containerized MCP services
├── agents/                         ← AI agents
├── microservices/                  ← FastAPI service
├── ui/                             ← Streamlit UI
├── orchestration/                  ← LangGraph workflow
└── utils/                          ← Utilities & config
```

---

## Performance Metrics

**Deployment Time:**
- First run (with build): ~2-3 minutes
- Subsequent runs: ~10-15 seconds

**Service Startup Order:**
1. MCP Servers (8001, 8002) - ~3 seconds
2. Decision Synthesis (8003) - ~5 seconds
3. Notification System (8004) - ~3 seconds
4. FastAPI Service (8000) - ~5 seconds
5. Streamlit UI (8501) - ~10 seconds

**System Ready:** ~30-40 seconds after initial startup

---

## Production Deployment Options

### Local Docker
```bash
docker-compose up -d --build
```

### Docker Swarm
```bash
docker stack deploy -c docker-compose.yml loan-approval
```

### Kubernetes
```bash
kompose convert -f docker-compose.yml -o k8s/
kubectl apply -f k8s/
```

### Cloud Platforms
- **AWS ECS:** `ecs-cli compose service up`
- **Google Cloud Run:** Upload to Artifact Registry
- **Azure Container Instances:** `az container create`

---

## What's New in Docker Support

✅ **Added Files:**
- `Dockerfile` - Builds optimized Python 3.11 slim image
- `docker-compose.yml` - Orchestrates 6 services with networking
- `.dockerignore` - Excludes unnecessary files from build
- `DOCKER_DEPLOYMENT.md` - Comprehensive Docker guide
- `DEPLOYMENT_QUICK_START.md` - This quick reference

✅ **Features:**
- Single-command deployment
- Automatic service health checks
- Inter-service networking
- Environment configuration
- Cross-platform support (Linux, Mac, Windows)
- Production-ready configuration

---

## Next Steps

1. **Install Docker** (if needed)
2. **Create .env file** with your API key
3. **Run:** `docker-compose up --build`
4. **Access:** http://localhost:8501
5. **Submit applications** and watch decisions in real-time!

---

## Support Resources

- **Detailed Docker Guide:** See [DOCKER_DEPLOYMENT.md](DOCKER_DEPLOYMENT.md)
- **General Documentation:** See [README.md](README.md)
- **Architecture Details:** See [ARCHITECTURE.md](ARCHITECTURE.md)
- **Testing Guide:** See [TESTING_GUIDE.md](TESTING_GUIDE.md)

---

**Ready?** Run this now:

```bash
docker-compose up --build
```

Then visit: http://localhost:8501 ✨
