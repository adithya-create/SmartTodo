import streamlit as st
import pandas as pd
from datetime import date, datetime
from utils.task_manager import get_all_tasks
from utils.history_manager import get_history
from utils.helper import (
    inject_custom_css,
    format_date,
    get_priority_color,
    get_category_icon,
    get_action_emoji,
    format_datetime
)

# Streamlit page layout configuration
st.set_page_config(
    page_title="SmartTodo - Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject CSS styling
inject_custom_css()

# Header
st.title("📊 Performance & Analytics Dashboard")
st.caption("Insights, productivity metrics, and task analytics.")
st.markdown("---")

# Load data
all_tasks = get_all_tasks()
all_logs = get_history()

# Compute metric aggregates
total_active = len([t for t in all_tasks if t["status"] != "Deleted"])
pending_count = len([t for t in all_tasks if t["status"] == "Pending"])
completed_count = len([t for t in all_tasks if t["status"] == "Completed"])
deleted_count = len([t for t in all_tasks if t["status"] == "Deleted"])
completion_percentage = (completed_count / total_active * 100) if total_active > 0 else 0.0

# -----------------
# 1. Metric Cards Grid
# -----------------
col_tot, col_pen, col_com, col_del, col_pct = st.columns(5)

with col_tot:
    st.metric(label="Total Active Tasks", value=total_active)
with col_pen:
    st.metric(label="Pending Tasks", value=pending_count, delta=f"{pending_count} remaining", delta_color="inverse")
with col_com:
    st.metric(label="Completed Tasks", value=completed_count, delta=f"{completed_count} done", delta_color="normal")
with col_del:
    st.metric(label="Deleted (Trash)", value=deleted_count)
with col_pct:
    st.metric(label="Completion Rate", value=f"{completion_percentage:.1f}%")

# -----------------
# 2. Progress Indicator
# -----------------
st.markdown("### 📈 Overall Completion Progress")
st.progress(completion_percentage / 100.0)
st.caption(f"{completed_count} of {total_active} active tasks completed.")

st.markdown("---")

# -----------------
# 3. Main Dashboard Content (Today's Tasks & Charts)
# -----------------
col_tasks, col_charts = st.columns([4, 5])

with col_tasks:
    st.subheader("📅 Due Today")
    today_str = date.today().strftime("%Y-%m-%d")
    
    todays_tasks = [
        t for t in all_tasks 
        if t["status"] != "Deleted" and t.get("deadline") == today_str
    ]
    
    if not todays_tasks:
        st.success("🎉 Clear schedule for today! No deadlines due today.")
    else:
        for task in todays_tasks:
            p_color = get_priority_color(task["priority"])
            cat_ico = get_category_icon(task["category"])
            status_symbol = "✅" if task["status"] == "Completed" else "⏳"
            
            st.markdown(
                f"""
                <div style="padding: 12px 16px; border-radius: 8px; margin-bottom: 10px; background: rgba(255,255,255,0.02); border-left: 4px solid {p_color}; border: 1px solid rgba(255,255,255,0.05);">
                    <span style="font-size:0.85rem; color:{p_color}; font-weight:700;">{task['priority'].upper()}</span>
                    <h5 style="margin: 4px 0;">{status_symbol} {task['title']}</h5>
                    <p style="margin:0; font-size:0.85rem; opacity:0.8;">{cat_ico} {task['category']} | Deadline: {format_date(task['deadline'])}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("### 📋 Category Distribution")
    # Generate Pandas distribution data
    active_tasks = [t for t in all_tasks if t["status"] != "Deleted"]
    if not active_tasks:
        st.info("No active tasks available to generate charts.")
    else:
        df = pd.DataFrame(active_tasks)
        cat_counts = df.groupby("category").size().reset_index(name="Count")
        cat_counts = cat_counts.set_index("category")
        st.bar_chart(cat_counts)

with col_charts:
    st.subheader("📊 Task Breakdown")
    if active_tasks:
        df = pd.DataFrame(active_tasks)
        
        # Priority distribution vs status
        prio_status = df.groupby(["priority", "status"]).size().unstack(fill_value=0)
        # Reindex to force standard priority levels ordering
        prio_levels = ["Low", "Medium", "High"]
        prio_status = prio_status.reindex(prio_levels, fill_value=0)
        
        # Ensure status columns exist in df
        for status_val in ["Pending", "Completed"]:
            if status_val not in prio_status.columns:
                prio_status[status_val] = 0
                
        st.markdown("**Priority Status Breakdown**")
        st.bar_chart(prio_status[["Pending", "Completed"]])
        
        # Category vs Status breakdown
        cat_status = df.groupby(["category", "status"]).size().unstack(fill_value=0)
        for status_val in ["Pending", "Completed"]:
            if status_val not in cat_status.columns:
                cat_status[status_val] = 0
                
        st.markdown("**Category Status Breakdown**")
        st.bar_chart(cat_status[["Pending", "Completed"]])
    else:
        st.info("Create tasks to visualize status charts.")

# -----------------
# 4. Recent Activity Log Section
# -----------------
st.markdown("---")
st.subheader("🔔 Recent Activity Audit")

recent_logs = all_logs[:5] # fetch top 5 logs
if not recent_logs:
    st.info("No activity records registered yet.")
else:
    for log in recent_logs:
        act = log["action"]
        emoji = get_action_emoji(act)
        time_formatted = format_datetime(log["timestamp"])
        
        st.markdown(
            f"""
            <div style="padding: 10px 16px; border-radius: 8px; margin-bottom: 8px; background: rgba(255,255,255,0.01); border: 1px solid rgba(255,255,255,0.03);">
                <span style="font-size:0.75rem; opacity:0.6;">⏱️ {time_formatted}</span>
                <span style="font-weight:600; margin-left: 10px;">{emoji} {act}</span>
                <span style="margin-left: 15px; opacity:0.8;">— {log['task_title']} <code>({log['task_id'][:8]})</code></span>
            </div>
            """,
            unsafe_allow_html=True
        )
