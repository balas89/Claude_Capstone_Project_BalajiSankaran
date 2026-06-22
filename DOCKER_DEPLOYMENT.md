# Docker Deployment Guide

## Overview

The Multi-Agent Agentic AI Loan Approval System is fully containerized for production deployment using Docker and docker-compose.

---

## Quick Start (Single Command)

### Prerequisites
- Docker installed ([download here](https://www.docker.com/products/docker-desktop))
- Docker Compose installed (included with Docker Desktop)
- `.env` file configured with `ANTHROPIC_API_KEY`

### One-Line Deployment

```bash
docker-compose up --build
```

**That's it!** This single command will:
1. Build all 6 service Docker images
2. Start all containerized services with correct networking
3. Initialize all MCP servers (ports 8001-8004)
4. Start FastAPI microservice (port 8000)
5. Launch Streamlit UI (port 8501)
6. Set up inter-service communication automatically

---

## Architecture

### Containerized Services

```
┌─────────────────────────────────────────────────────┐
│         Docker Compose Network                      │
│      (loan-approval-network - bridge)              │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌─────────────────────────────────────────────┐  │
│  │  Streamlit UI (Port 8501)                   │  │
│  │  - Interactive chatbot interface            │  │
│  │  - Real-time decision display               │  │
│  └──────────────────┬──────────────────────────┘  │
│                     │                              │
│  ┌──────────────────▼──────────────────────────┐  │
│  │  FastAPI Microservice (Port 8000)           │  │
│  │  - Main orchestration endpoint               │  │
│  │  - Request validation & routing              │  │
│  └──────────────────┬──────────────────────────┘  │
│                     │                              │
│         ┌───────────┼───────────┐                  │
│         │           │           │                  │
│   ┌─────▼────┐ ┌───▼─────┐ ┌──▼──────┐            │
│   │ Applicant│ │  Risk   │ │Decision │            │
│   │ DB MCP   │ │ Rules   │ │Synthesis│            │
│   │(8001)    │ │ MCP     │ │ MCP     │            │
│   │          │ │(8002)   │ │(8003)   │            │
│   └──────────┘ └─────────┘ └─────────┘            │
│         │           │           │                  │
│         └───────────┼───────────┘                  │
│                     │                              │
│              ┌──────▼──────┐                       │
│              │Notification │                       │
│              │System MCP   │                       │
│              │(8004)       │                       │
│              └─────────────┘                       │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### Service Details

| Service | Container | Port | Health Check | Dependencies |
|---------|-----------|------|--------------|--------------|
| Streamlit UI | loan-approval-ui | 8501 | HTTP /health | fastapi-service |
| FastAPI | loan-approval-api | 8000 | HTTP /health | All MCP servers |
| Applicant DB MCP | applicant-db-server | 8001 | HTTP /health | None |
| Risk Rules MCP | risk-rules-db-server | 8002 | HTTP /health | None |
| Decision Synthesis MCP | decision-synthesis-server | 8003 | HTTP /health | applicant-db, risk-rules-db |
| Notification System MCP | notification-system-server | 8004 | HTTP /health | All upstream services |

---

## Common Commands

### Start All Services (with rebuild)
```bash
docker-compose up --build
```

### Start All Services (without rebuild)
```bash
docker-compose up
```

### Start in Background (detached mode)
```bash
docker-compose up -d --build
```

### Stop All Services
```bash
docker-compose down
```

### Stop and Remove Volumes
```bash
docker-compose down -v
```

### View Running Containers
```bash
docker-compose ps
```

### View Logs for All Services
```bash
docker-compose logs -f
```

### View Logs for Specific Service
```bash
docker-compose logs -f fastapi-service
docker-compose logs -f streamlit-ui
docker-compose logs -f applicant-db
```

### Restart a Specific Service
```bash
docker-compose restart fastapi-service
```

### Execute Command in Container
```bash
docker-compose exec fastapi-service python test_api.py
```

---

## Environment Configuration

### Create .env File

Before running, create a `.env` file in the project root with:

```bash
# Anthropic API Configuration
ANTHROPIC_API_KEY=sk-your-api-key-here

# Service URLs (automatically set by docker-compose)
APPLICANT_DB_URL=http://applicant-db:8001
RISK_RULES_DB_URL=http://risk-rules-db:8002
DECISION_SYNTHESIS_URL=http://decision-synthesis:8003
NOTIFICATION_SYSTEM_URL=http://notification-system:8004

# FastAPI Configuration
FASTAPI_HOST=0.0.0.0
FASTAPI_PORT=8000

# Streamlit Configuration
STREAMLIT_SERVER_PORT=8501
```

Or copy from example:
```bash
cp .env.example .env
# Then edit .env with your ANTHROPIC_API_KEY
```

---

## Accessing Services

### After docker-compose up completes:

| Service | URL | Purpose |
|---------|-----|---------|
| Streamlit UI | http://localhost:8501 | User interface for loan applications |
| FastAPI API | http://localhost:8000 | REST API endpoints |
| API Docs | http://localhost:8000/docs | Interactive API documentation (Swagger UI) |
| Applicant DB | http://localhost:8001/docs | Applicant database service API docs |
| Risk Rules DB | http://localhost:8002/docs | Risk rules service API docs |
| Decision Synthesis | http://localhost:8003/docs | Decision synthesis service API docs |
| Notification System | http://localhost:8004/docs | Notification service API docs |

---

## Health Checks

Each service includes automatic health checks. View container status:

```bash
# Check container health
docker-compose ps

# View detailed health status
docker inspect loan-approval-api --format='{{.State.Health.Status}}'
```

Services will automatically restart if health checks fail (3 retries with 10s intervals).

---

## Testing

### Test All Endpoints (inside container)

```bash
# Execute test suite in fastapi-service container
docker-compose exec fastapi-service python test_api.py
```

### Test Single Endpoint (curl from host)

```bash
# Health check
curl http://localhost:8000/health

# Submit loan application
curl -X POST http://localhost:8000/apply-loan \
  -H "Content-Type: application/json" \
  -d '{
    "applicant_id": "APP001",
    "name": "John Doe",
    "email": "john@example.com",
    "income": 75000,
    "employment_years": 5,
    "credit_score": 720,
    "loan_amount": 250000,
    "employment_type": "Full-time",
    "credit_history": "Good"
  }'
```

---

## Troubleshooting

### Services Not Starting

```bash
# View all logs
docker-compose logs

# View specific service logs
docker-compose logs fastapi-service

# Check for errors
docker-compose logs --tail=50 fastapi-service
```

### Port Already in Use

If ports are already in use, modify `docker-compose.yml`:

```yaml
ports:
  - "9000:8000"  # Map to different host port
```

### ANTHROPIC_API_KEY Not Set

```bash
# Verify .env file exists
ls -la .env

# Set inline (temporary)
ANTHROPIC_API_KEY=sk-xxx docker-compose up --build
```

### Container Exited Unexpectedly

```bash
# View container logs
docker-compose logs <service-name>

# Rebuild image
docker-compose build --no-cache <service-name>

# Restart service
docker-compose up --build <service-name>
```

---

## Production Considerations

### Security Hardening

1. **API Authentication**
   - Add JWT token validation
   - Implement rate limiting
   - Use HTTPS/TLS

2. **Database Persistence**
   - Replace mock databases with PostgreSQL
   - Add Docker volume for data persistence
   - Implement backup strategy

3. **Environment Secrets**
   - Use Docker Secrets for sensitive data
   - Never commit `.env` to version control
   - Use separate `.env.prod` for production

4. **Logging & Monitoring**
   - Integrate with ELK Stack
   - Add Prometheus metrics
   - Set up Grafana dashboards
   - Configure alerting

### Performance Optimization

1. **Resource Limits**
   ```yaml
   resources:
     limits:
       cpus: '1'
       memory: 512M
   ```

2. **Auto-Scaling**
   - Use Docker Swarm or Kubernetes
   - Load balance across service replicas
   - Implement health-based scaling

3. **Caching**
   - Add Redis container for result caching
   - Cache credit history and risk rules

---

## Deployment Platforms

### Local Development
```bash
docker-compose up --build
```

### Docker Hub Registry

Build and push images:
```bash
docker build -t balas89/loan-approval:latest .
docker push balas89/loan-approval:latest
```

### Docker Swarm

Deploy stack:
```bash
docker stack deploy -c docker-compose.yml loan-approval
```

### Kubernetes

Convert compose file to Kubernetes:
```bash
kompose convert -f docker-compose.yml -o k8s/
kubectl apply -f k8s/
```

### AWS (ECS)

```bash
# Use ECS Compose Extension
docker compose -f docker-compose.yml up
```

### Google Cloud (Cloud Run)

Build and deploy:
```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/loan-approval
gcloud run deploy loan-approval --image gcr.io/PROJECT_ID/loan-approval
```

---

## Advanced Usage

### Run Specific Services Only

```bash
# Run only Streamlit and FastAPI (skip MCP servers)
docker-compose up streamlit-ui fastapi-service
```

### Run with Custom Configuration

```bash
# Override environment variables
docker-compose -e FASTAPI_PORT=9000 up

# Use different compose file
docker-compose -f docker-compose.prod.yml up
```

### View Resource Usage

```bash
# Monitor container resource usage
docker stats

# Specific container
docker stats loan-approval-api
```

---

## Cleanup

### Remove All Containers and Networks

```bash
docker-compose down
```

### Remove Everything Including Volumes

```bash
docker-compose down -v
```

### Remove Unused Images

```bash
docker image prune -a
```

### Full System Cleanup

```bash
docker system prune -a --volumes
```

---

## Files Included

- **Dockerfile** - Multi-stage build for all services
- **docker-compose.yml** - Complete orchestration configuration
- **.dockerignore** - Exclude unnecessary files from image
- **DOCKER_DEPLOYMENT.md** - This guide

---

## Support

For issues or questions:
1. Check logs: `docker-compose logs <service-name>`
2. Verify .env configuration
3. Ensure Docker and docker-compose are up to date
4. Review service health checks: `docker-compose ps`

---

**Ready to deploy!** Use: `docker-compose up --build`
