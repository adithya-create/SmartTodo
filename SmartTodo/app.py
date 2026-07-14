import streamlit as st
import os
from dotenv import load_dotenv
from utils.database import initialize_db
from utils.validator import validate_env_setup, check_db_health
from utils.helper import inject_custom_css

# Load environment configurations
load_dotenv()

# Streamlit page layout configuration
st.set_page_config(
    page_title="SmartTodo - Home",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject custom UI css
inject_custom_css()

# Initialize databases
initialize_db()

# Run validation checks
env_ok, env_errors = validate_env_setup()
db_ok, db_msg = check_db_health()

# Initialize core session states
if "app_name" not in st.session_state:
    st.session_state.app_name = os.getenv("APP_NAME", "SmartTodo")
if "app_version" not in st.session_state:
    st.session_state.app_version = os.getenv("APP_VERSION", "1.0.0")

# Render UI Title and Subtitle
st.title("🎯 SmartTodo")
st.caption(f"v{st.session_state.app_version} | Professional Task Management Suite")

# Display validation results
if not env_ok:
    st.error("🚨 Environmental Configuration Validation Failed!")
    for err in env_errors:
        st.write(f"- {err}")
    st.warning("Please check your `.env` configuration file in the project root directory.")
    st.stop()

# Layout layout split
col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("Welcome to your Smart Workspace")
    st.markdown(
        """
        SmartTodo is a production-ready personal planner application built on a robust local JSON file engine.
        Using the sidebar navigation menu on the left, you can access the following modules:
        
        *   **💼 Task Manager**: Add new tasks, edit fields, search/filter/sort, toggle status, download JSON, and soft-delete/restore records.
        *   **📋 Audit History**: Retrieve chronological audit trails of all updates, creations, and completions. Download or clear logs.
        *   **📊 Performance Dashboard**: Monitor task completion rates, view deadlines due today, track active progress indicators, and analyze productivity metrics.
        """
    )
    
    st.info("👈 Open the sidebar to select a page and start managing your workflow.")

with col2:
    st.subheader("System Health Diagnostics")
    
    # Render indicators
    st.success("✅ Environment configuration validated successfully.")
    
    if db_ok:
        st.success(f"✅ {db_msg}")
    else:
        st.warning(f"⚠️ {db_msg}")
        
    st.markdown("---")
    st.markdown("### Application Details")
    st.json({
        "Application": st.session_state.app_name,
        "Version": st.session_state.app_version,
        "Storage Engine": "Atomic JSON File Database",
        "Python Version": "3.11+",
        "Environment Load": "Success"
    })
