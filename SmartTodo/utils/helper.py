import json
from datetime import datetime
from typing import Any

def inject_custom_css() -> None:
    """
    Injects custom CSS from assets/style.css into Streamlit UI.
    """
    import streamlit as st
    import os
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    css_path = os.path.join(base_dir, "assets", "style.css")
    if os.path.exists(css_path):
        try:
            with open(css_path, "r", encoding="utf-8") as f:
                css_content = f.read()
            st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
        except Exception:
            # Prevent crashes if assets/style.css fails to load
            pass

def format_datetime(iso_str: str | None) -> str:
    """
    Converts an ISO format date-time string to a human-readable format.
    Example: '2026-07-14T21:41:00' -> 'Jul 14, 2026 09:41 PM'
    """
    if not iso_str:
        return "N/A"
    try:
        cleaned_str = iso_str.replace("Z", "+00:00")
        dt = datetime.fromisoformat(cleaned_str)
        return dt.strftime("%b %d, %Y %I:%M %p")
    except Exception:
        return str(iso_str)

def format_date(date_str: str | None) -> str:
    """
    Formats a date string ('YYYY-MM-DD') into 'MMM DD, YYYY'.
    Example: '2026-07-14' -> 'Jul 14, 2026'
    """
    if not date_str:
        return "No Deadline"
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return dt.strftime("%b %d, %Y")
    except Exception:
        return str(date_str)

def get_priority_color(priority: str) -> str:
    """Returns CSS color style for priority level."""
    colors = {
        "High": "#FF4B4B",     # Streamlit Red
        "Medium": "#FF9800",   # Orange
        "Low": "#4CAF50"       # Green
    }
    return colors.get(priority, "#9E9E9E")

def get_category_icon(category: str) -> str:
    """Returns an emoji associated with a category."""
    icons = {
        "Work": "💼",
        "Personal": "👤",
        "Shopping": "🛒",
        "Health": "❤️",
        "Education": "🎓",
        "Finance": "💵",
        "Fitness": "🏃",
        "Others": "📌"
    }
    return icons.get(category, "📌")

def get_action_emoji(action: str) -> str:
    """Returns an emoji associated with history action."""
    emojis = {
        "Task Created": "🆕",
        "Task Updated": "✏️",
        "Task Deleted": "🗑️",
        "Task Restored": "🔄",
        "Task Completed": "✅",
        "Task Reopened": "🔓",
        "Completed Tasks Cleared": "🧹"
    }
    return emojis.get(action, "ℹ️")

def to_json_string(data: Any) -> str:
    """Converts python objects to pretty JSON string for downloadeable resources."""
    try:
        return json.dumps(data, indent=4)
    except Exception:
        return "[]"
