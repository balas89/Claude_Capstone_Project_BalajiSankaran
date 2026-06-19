"""FastAPI main application"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from microservices.routes import router
from utils.config import FASTAPI_HOST, FASTAPI_PORT

app = FastAPI(
    title="Loan Approval System API",
    description="Multi-Agent Agentic AI Loan Approval System",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router)

@app.get("/")
async def root():
    return {
        "message": "Loan Approval System API",
        "version": "1.0.0",
        "endpoints": {
            "apply_loan": "POST /apply-loan",
            "health": "GET /health",
            "docs": "GET /docs",
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=FASTAPI_HOST,
        port=FASTAPI_PORT,
        reload=False
    )
