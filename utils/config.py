import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
MODEL_NAME = "claude-sonnet-4-20250514"

# Service URLs
APPLICANT_DB_URL = os.getenv("APPLICANT_DB_URL", "http://localhost:8001")
RISK_RULES_DB_URL = os.getenv("RISK_RULES_DB_URL", "http://localhost:8002")
DECISION_SYNTHESIS_URL = os.getenv("DECISION_SYNTHESIS_URL", "http://localhost:8003")
NOTIFICATION_SYSTEM_URL = os.getenv("NOTIFICATION_SYSTEM_URL", "http://localhost:8004")

# FastAPI Configuration
FASTAPI_HOST = os.getenv("FASTAPI_HOST", "0.0.0.0")
FASTAPI_PORT = int(os.getenv("FASTAPI_PORT", "8000"))

# Streamlit Configuration
STREAMLIT_SERVER_PORT = int(os.getenv("STREAMLIT_SERVER_PORT", "8501"))

# Loan Rules
MIN_INCOME = 20000
MAX_LOAN_AMOUNT = 500000
MIN_CREDIT_SCORE = 300
MAX_CREDIT_SCORE = 850
RECOMMENDED_DTI_THRESHOLD = 0.43
CRITICAL_DTI_THRESHOLD = 0.50

# Risk Thresholds
HIGH_RISK_SCORE_THRESHOLD = 0.7
MEDIUM_RISK_SCORE_THRESHOLD = 0.4
