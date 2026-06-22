"""Streamlit Chatbot UI for Loan Application"""
import streamlit as st
import requests
import json
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Loan Approval System",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Styling
st.markdown("""
    <style>
    .main-header { font-size: 2.5rem; color: #1f77b4; font-weight: bold; }
    .sub-header { font-size: 1.5rem; color: #555; }
    .decision-approve { color: #2ecc71; font-weight: bold; font-size: 1.3rem; }
    .decision-reject { color: #e74c3c; font-weight: bold; font-size: 1.3rem; }
    .decision-review { color: #f39c12; font-weight: bold; font-size: 1.3rem; }
    </style>
""", unsafe_allow_html=True)

# API Configuration
API_BASE_URL = "http://localhost:8000"

st.markdown("<div class='main-header'>🏦 Loan Approval System</div>", unsafe_allow_html=True)
st.markdown("Multi-Agent Agentic AI for Intelligent Loan Decisions")
st.divider()

# Sidebar
with st.sidebar:
    st.markdown("## 📋 System Status")

    try:
        health_response = requests.get(f"{API_BASE_URL}/health", timeout=2)
        if health_response.status_code == 200:
            st.success("✅ System Online")
        else:
            st.error("❌ API Unavailable")
    except:
        st.error("❌ Cannot reach API")

    st.markdown("---")
    st.markdown("## ℹ️ About")
    st.info("""
    This system uses multiple AI agents to analyze loan applications:
    - **Applicant Profile Agent**: Analyzes applicant details
    - **Financial Risk Agent**: Evaluates financial metrics
    - **Loan Decision Agent**: Synthesizes decision using Claude
    - **Compliance Agent**: Ensures regulatory compliance
    """)

# Main content - Two columns
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("### 📝 Application Form")

    with st.form("loan_application_form"):
        st.markdown("#### 👤 Personal Information")
        col_a1, col_a2, col_a3 = st.columns(3)
        with col_a1:
            applicant_id = st.text_input("Applicant ID", value="APP001")
        with col_a2:
            age = st.number_input("Age", min_value=18, max_value=100, value=35)
        with col_a3:
            location = st.selectbox("Location", ["New York", "California", "Texas", "Florida", "Other"])

        st.markdown("#### 💰 Financial Information")
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            income = st.number_input("Annual Income ($)", min_value=20000, max_value=500000, value=80000, step=5000)
        with col_f2:
            credit_score = st.number_input("Credit Score", min_value=300, max_value=850, value=720)
        with col_f3:
            existing_liabilities = st.number_input("Monthly Liabilities ($)", min_value=0, max_value=500000, value=2500, step=500)

        st.markdown("#### 💼 Employment & Loan Details")
        col_e1, col_e2 = st.columns(2)
        with col_e1:
            employment_type = st.selectbox("Employment Type", ["Salaried", "Self-Employed", "Freelance", "Retired"])
        with col_e2:
            loan_amount = st.number_input("Requested Loan Amount ($)", min_value=10000, max_value=500000, value=150000, step=10000)

        col_l1, col_l2 = st.columns(2)
        with col_l1:
            tenure_months = st.number_input("Loan Tenure (months)", min_value=6, max_value=360, value=60, step=6)
        with col_l2:
            st.empty()

        submit_button = st.form_submit_button("🚀 Submit Application", use_container_width=True)

with col2:
    st.markdown("### 📊 Decision Results")

    if submit_button:
        # Prepare application data
        application_data = {
            "applicant_id": applicant_id,
            "age": age,
            "income": income,
            "employment_type": employment_type,
            "credit_score": credit_score,
            "loan_amount": loan_amount,
            "tenure_months": tenure_months,
            "existing_liabilities": existing_liabilities,
            "location": location,
        }

        # Show processing status
        with st.spinner("⏳ Processing application through agents..."):
            try:
                response = requests.post(
                    f"{API_BASE_URL}/apply-loan",
                    json=application_data,
                    timeout=60
                )

                if response.status_code == 200:
                    result = response.json()

                    # Display decision
                    decision = result.get("decision", "Unknown")
                    risk_score = result.get("risk_score", 0)
                    confidence = result.get("confidence", 0)

                    st.success("✅ Application Processed Successfully")

                    # Decision highlight
                    if decision == "Approve":
                        st.markdown(f"<div class='decision-approve'>✅ APPROVED</div>", unsafe_allow_html=True)
                    elif decision == "Reject":
                        st.markdown(f"<div class='decision-reject'>❌ REJECTED</div>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<div class='decision-review'>⚠️ REQUIRES MANUAL REVIEW</div>", unsafe_allow_html=True)

                    st.divider()

                    # Key metrics
                    metric_col1, metric_col2, metric_col3 = st.columns(3)
                    with metric_col1:
                        st.metric("Risk Score", f"{risk_score:.2%}")
                    with metric_col2:
                        st.metric("Confidence", f"{confidence:.2%}")
                    with metric_col3:
                        st.metric("Case ID", result.get("case_id", "N/A")[:8] + "...")

                    st.divider()

                    # Explanation
                    st.markdown("**📋 Decision Explanation:**")
                    st.write(result.get("explanation", "No explanation provided"))

                    st.divider()

                    # Key factors
                    st.markdown("**🔍 Key Decision Factors:**")
                    factors = result.get("factors", [])
                    for factor in factors:
                        st.write(f"• {factor}")

                    st.divider()

                    # Detailed Analysis Tabs
                    tab1, tab2, tab3, tab4 = st.tabs(
                        ["Profile Analysis", "Financial Analysis", "Compliance", "Full Details"]
                    )

                    with tab1:
                        profile = result.get("profile_analysis", {})
                        if profile:
                            st.metric("Income Stability Score", f"{profile.get('income_stability_score', 0):.2%}")
                            st.metric("Employment Risk", profile.get("employment_risk", "N/A"))
                            st.write("**Credit History:**")
                            credit_hist = profile.get("credit_history_summary", {})
                            for key, value in credit_hist.items():
                                st.write(f"• {key}: {value}")

                    with tab2:
                        financial = result.get("financial_analysis", {})
                        if financial:
                            st.metric("DTI Ratio", f"{financial.get('dti_ratio', 0):.3f}")
                            st.metric("Credit Risk Level", financial.get("credit_risk_level", "N/A"))
                            st.metric("Loan Amount Risk", financial.get("loan_amount_risk", "N/A"))
                            st.write("**Anomalies Detected:**")
                            for anomaly in financial.get("anomalies", []):
                                st.warning(f"⚠️ {anomaly}")

                    with tab3:
                        compliance = result.get("compliance_status", {})
                        if compliance:
                            st.write(f"**Action Taken:** {compliance.get('action_taken', 'N/A')}")
                            st.write(f"**Notification Sent:** {'✅ Yes' if compliance.get('notification_sent') else '❌ No'}")
                            st.write(f"**Timestamp:** {compliance.get('timestamp', 'N/A')}")

                    with tab4:
                        st.json(result)
                else:
                    st.error(f"API Error: {response.status_code}")
                    st.write(response.text)

            except requests.exceptions.Timeout:
                st.error("⏱️ Request timed out. Please try again.")
            except requests.exceptions.ConnectionError:
                st.error("🔌 Cannot connect to API. Ensure the microservice is running on localhost:8000")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

st.divider()

# History section (stored in session state)
if "application_history" not in st.session_state:
    st.session_state.application_history = []

if submit_button and response.status_code == 200:
    st.session_state.application_history.insert(0, {
        "timestamp": datetime.now().isoformat(),
        "applicant_id": applicant_id,
        "age": age,
        "income": income,
        "credit_score": credit_score,
        "employment_type": employment_type,
        "loan_amount": loan_amount,
        "tenure_months": tenure_months,
        "existing_liabilities": existing_liabilities,
        "location": location,
        "decision": result.get("decision"),
        "risk_score": result.get("risk_score"),
        "case_id": result.get("case_id"),
    })

if st.session_state.application_history:
    st.markdown("### 📜 Application History (Session)")
    for idx, app in enumerate(st.session_state.application_history[:10]):
        decision_icon = "✅" if app["decision"] == "Approve" else "❌" if app["decision"] == "Reject" else "⚠️"
        st.write(f"{decision_icon} {app['case_id']} - {app['applicant_id']} | Age: {app['age']} | Income: ${app['income']:,.0f} | Credit: {app['credit_score']} | Loan: ${app['loan_amount']:,.0f} | Tenure: {app['tenure_months']}m | DTI Risk: {app['risk_score']:.1%}")
