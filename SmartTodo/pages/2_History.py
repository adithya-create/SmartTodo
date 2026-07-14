import streamlit as st
from datetime import datetime
from utils.history_manager import get_history, clear_history
from utils.helper import inject_custom_css, format_datetime, get_action_emoji, to_json_string

# Streamlit Page configuration
st.set_page_config(
    page_title="SmartTodo - History",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject CSS styles
inject_custom_css()

# Title
st.title("📋 Operational Audit History")
st.caption("Track, inspect, and audit all task database modifications in real-time.")
st.markdown("---")

# Fetch all logs
logs = get_history()

# -----------------
# 1. Search & Filter Controls
# -----------------
st.subheader("🔍 Filter Audit Trails")
col_search, col_action = st.columns([2, 1])

with col_search:
    search_q = st.text_input("Search Logs", placeholder="Search by title, description, or action...")

with col_action:
    action_filter = st.selectbox(
        "Action Filter",
        ["All", "Task Created", "Task Updated", "Task Deleted", "Task Restored", "Task Completed", "Task Reopened", "Completed Tasks Cleared"]
    )

# Apply filters
filtered_logs = logs

if action_filter != "All":
    filtered_logs = [l for l in filtered_logs if l["action"] == action_filter]

if search_q:
    sq = search_q.lower()
    filtered_logs = [
        l for l in filtered_logs
        if sq in l.get("task_title", "").lower()
        or sq in l.get("description", "").lower()
        or sq in l.get("action", "").lower()
    ]

# -----------------
# 2. History Utilities
# -----------------
st.markdown("---")
col_clear, col_dl, _ = st.columns([2, 2.5, 5.5])

with col_clear:
    # Safety checkbox before clear trigger
    confirm_clear = st.checkbox("Enable clearing history")
    if st.button("🧹 Clear History", disabled=not confirm_clear, help="Delete all audit log records permanently."):
        if clear_history():
            st.success("Operational logs cleared successfully!")
            st.rerun()

with col_dl:
    history_json_str = to_json_string(logs)
    st.download_button(
        label="📥 Download History logs as JSON",
        data=history_json_str,
        file_name=f"smarttodo_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        mime="application/json"
    )

# -----------------
# 3. Timeline Render
# -----------------
st.markdown("---")
st.subheader("⏱️ Recent Activity Timeline")

if not filtered_logs:
    st.info("💡 No logs match the selected filter configuration.")
else:
    # Wrap in custom css container
    st.markdown('<div class="timeline-wrapper">', unsafe_allow_html=True)
    
    for idx, log in enumerate(filtered_logs):
        action = log["action"]
        emoji = get_action_emoji(action)
        time_display = format_datetime(log["timestamp"])
        
        # Match timeline marker styles
        css_marker_class = "event-info"
        if action == "Task Created":
            css_marker_class = "event-create"
        elif action == "Task Updated":
            css_marker_class = "event-update"
        elif action == "Task Deleted":
            css_marker_class = "event-delete"
        elif action == "Task Restored":
            css_marker_class = "event-restore"
        elif action == "Task Completed":
            css_marker_class = "event-complete"
        elif action == "Task Reopened":
            css_marker_class = "event-reopen"
        
        prev_st = log.get("previous_status") or "None"
        curr_st = log.get("current_status") or "None"
        
        # Format task target display
        if log["task_id"] == "system-clear":
            target_str = "<strong>System Event</strong>"
        else:
            display_id = log["task_id"][:8] if log["task_id"] else "unknown"
            target_str = f"Task: <strong>{log['task_title']}</strong> <code style='font-size:0.75rem;'>({display_id})</code>"

        description_text = log.get("description", "").strip()
        
        st.markdown(
            f"""
            <div class="timeline-event {css_marker_class}">
                <div style="font-size: 0.8rem; opacity: 0.65; margin-bottom: 2px;">⏱️ {time_display}</div>
                <h4 style="margin: 0 0 6px 0; font-size:1.1rem; font-weight:600;">{emoji} {action}</h4>
                <div style="font-size: 0.95rem; margin-bottom: 6px;">{target_str}</div>
                <div style="font-size: 0.9rem; padding: 10px 14px; border-radius: 8px; background: rgba(255,255,255,0.015); border: 1px solid rgba(255,255,255,0.04);">
                    {description_text if description_text else 'No additional details provided.'}
                    <div style="margin-top: 6px; font-size: 0.75rem; opacity: 0.5;">
                        Status Transition: <code>{prev_st}</code> &rarr; <code>{curr_st}</code>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    st.markdown('</div>', unsafe_allow_html=True)
