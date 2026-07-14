import streamlit as st
from datetime import datetime, date
from utils.task_manager import (
    get_all_tasks,
    create_task,
    update_task,
    delete_task,
    restore_task,
    toggle_task_status,
    clear_completed_tasks
)
from utils.validator import validate_task_input
from utils.helper import (
    inject_custom_css,
    format_date,
    get_priority_color,
    get_category_icon,
    to_json_string
)

# Streamlit Page Config
st.set_page_config(
    page_title="SmartTodo - Task Manager",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject styling
inject_custom_css()

# Session State for edit tracking
if "editing_task_id" not in st.session_state:
    st.session_state.editing_task_id = None

# Header
st.title("💼 Task Manager")
st.caption("Manage, organize, filter, and track your daily tasks.")
st.markdown("---")

# Load fresh tasks
all_tasks = get_all_tasks()

# -----------------
# 1. Edit Task Section
# -----------------
if st.session_state.editing_task_id:
    editing_task = next((t for t in all_tasks if t["id"] == st.session_state.editing_task_id), None)
    if editing_task:
        st.subheader("✏️ Edit Task")
        
        # Load existing deadline if any
        existing_deadline_str = editing_task.get("deadline")
        try:
            default_deadline_date = (
                datetime.strptime(existing_deadline_str, "%Y-%m-%d").date()
                if existing_deadline_str
                else date.today()
            )
            has_deadline = existing_deadline_str is not None
        except ValueError:
            default_deadline_date = date.today()
            has_deadline = False
            
        with st.form("edit_task_form"):
            edit_title = st.text_input("Task Title", value=editing_task.get("title", ""))
            edit_desc = st.text_area("Description", value=editing_task.get("description", ""))
            
            col_cat, col_prio, col_dl = st.columns(3)
            with col_cat:
                edit_category = st.selectbox(
                    "Category",
                    ["Work", "Personal", "Shopping", "Health", "Education", "Finance", "Fitness", "Others"],
                    index=["Work", "Personal", "Shopping", "Health", "Education", "Finance", "Fitness", "Others"].index(
                        editing_task.get("category", "Work")
                    )
                )
            with col_prio:
                edit_priority = st.selectbox(
                    "Priority",
                    ["Low", "Medium", "High"],
                    index=["Low", "Medium", "High"].index(editing_task.get("priority", "Medium"))
                )
            with col_dl:
                edit_has_dl = st.checkbox("Set Deadline", value=has_deadline)
                edit_dl_val = st.date_input("Deadline Date", value=default_deadline_date)
            
            edit_status = st.selectbox(
                "Status",
                ["Pending", "Completed"],
                index=["Pending", "Completed"].index(
                    editing_task.get("status") if editing_task.get("status") != "Deleted" else "Pending"
                )
            )

            c1, c2 = st.columns([1, 6])
            with c1:
                submit_edit = st.form_submit_button("Save Changes")
            with c2:
                cancel_edit = st.form_submit_button("Cancel")

            if submit_edit:
                dl_date_str = edit_dl_val.strftime("%Y-%m-%d") if edit_has_dl else None
                # Validate input
                is_valid, err_msg = validate_task_input(
                    title=edit_title,
                    category=edit_category,
                    deadline_val=dl_date_str,
                    existing_tasks=all_tasks,
                    edit_task_id=editing_task["id"]
                )
                if not is_valid:
                    st.error(f"❌ {err_msg}")
                else:
                    updates = {
                        "title": edit_title,
                        "description": edit_desc,
                        "priority": edit_priority,
                        "category": edit_category,
                        "deadline": dl_date_str,
                        "status": edit_status
                    }
                    if update_task(editing_task["id"], updates):
                        st.success("🎉 Task updated successfully!")
                        st.session_state.editing_task_id = None
                        st.rerun()
                    else:
                        st.error("❌ Failed to update task. Please try again.")

            if cancel_edit:
                st.session_state.editing_task_id = None
                st.rerun()
        st.markdown("---")

# -----------------
# 2. Create Task Section
# -----------------
with st.expander("➕ Create New Task", expanded=False):
    with st.form("create_task_form"):
        new_title = st.text_input("Task Title", placeholder="What needs to be done?")
        new_desc = st.text_area("Description", placeholder="Enter task details/notes...")
        
        col_cat, col_prio, col_dl = st.columns(3)
        with col_cat:
            new_category = st.selectbox(
                "Category",
                ["Work", "Personal", "Shopping", "Health", "Education", "Finance", "Fitness", "Others"]
            )
        with col_prio:
            new_priority = st.selectbox("Priority", ["Low", "Medium", "High"], index=1)
        with col_dl:
            new_has_dl = st.checkbox("Set Deadline", value=False)
            new_dl_val = st.date_input("Deadline Date", value=date.today())

        submit_create = st.form_submit_button("Create Task")
        
        if submit_create:
            dl_date_str = new_dl_val.strftime("%Y-%m-%d") if new_has_dl else None
            # Validate input
            is_valid, err_msg = validate_task_input(
                title=new_title,
                category=new_category,
                deadline_val=dl_date_str,
                existing_tasks=all_tasks
            )
            if not is_valid:
                st.error(f"❌ {err_msg}")
            else:
                created = create_task(
                    title=new_title,
                    description=new_desc,
                    priority=new_priority,
                    category=new_category,
                    deadline=dl_date_str
                )
                if created:
                    st.success("🎉 Task created successfully!")
                    st.rerun()
                else:
                    st.error("❌ Failed to save task to database.")

# -----------------
# 3. Filters & Search Section
# -----------------
st.subheader("🔍 Search & Filters")
filter_col1, filter_col2, filter_col3, filter_col4 = st.columns([2, 1, 1, 1])

with filter_col1:
    search_query = st.text_input("Search Tasks", placeholder="Type title or description...")

with filter_col2:
    status_filter = st.selectbox(
        "Status Filter",
        ["Active (Pending & Completed)", "Pending", "Completed", "Deleted", "All"]
    )

with filter_col3:
    priority_filter = st.selectbox(
        "Priority Filter",
        ["All", "High", "Medium", "Low"]
    )

with filter_col4:
    category_filter = st.selectbox(
        "Category Filter",
        ["All", "Work", "Personal", "Shopping", "Health", "Education", "Finance", "Fitness", "Others"]
    )

# Sorting Columns
sort_col1, sort_col2, sort_col3 = st.columns([1.5, 1.5, 3])
with sort_col1:
    sort_by = st.selectbox(
        "Sort By",
        ["Created Date", "Deadline", "Alphabetical (Title)"]
    )
with sort_col2:
    sort_order = st.selectbox("Sort Order", ["Ascending", "Descending"])

# Apply Filters
filtered_tasks = all_tasks

# Apply Status Filter
if status_filter == "Active (Pending & Completed)":
    filtered_tasks = [t for t in filtered_tasks if t["status"] in ["Pending", "Completed"]]
elif status_filter != "All":
    filtered_tasks = [t for t in filtered_tasks if t["status"] == status_filter]

# Apply Priority Filter
if priority_filter != "All":
    filtered_tasks = [t for t in filtered_tasks if t["priority"] == priority_filter]

# Apply Category Filter
if category_filter != "All":
    filtered_tasks = [t for t in filtered_tasks if t["category"] == category_filter]

# Apply Search Query
if search_query:
    q = search_query.lower()
    filtered_tasks = [
        t for t in filtered_tasks
        if q in t["title"].lower() or q in t["description"].lower()
    ]

# Apply Sorting
def get_sort_key(task):
    if sort_by == "Alphabetical (Title)":
        return task["title"].lower()
    elif sort_by == "Deadline":
        # Put tasks with no deadline at the end (or start depending on order)
        dl = task.get("deadline")
        if not dl:
            return "9999-12-31" if sort_order == "Ascending" else "0000-01-01"
        return dl
    else:  # Created Date
        return task.get("created_at", "")

is_reverse = (sort_order == "Descending")
filtered_tasks.sort(key=get_sort_key, reverse=is_reverse)

# -----------------
# 4. Task Grid/List Render
# -----------------
st.markdown("---")

if not filtered_tasks:
    st.info("💡 No tasks found matching current search/filter settings.")
else:
    for task in filtered_tasks:
        task_id = task["id"]
        cat_icon = get_category_icon(task["category"])
        prio_color = get_priority_color(task["priority"])
        
        # Display each task card inside a styled container
        st.markdown(
            f"""
            <div class="task-card" style="border-left: 6px solid {prio_color};">
                <span class="p-badge" style="background-color: {prio_color}25; color: {prio_color}; border: 1px solid {prio_color}45;">{task['priority']}</span>
                <strong>{cat_icon} {task['category']}</strong>
                <h4 style="margin: 8px 0 4px 0;">{task['title']}</h4>
                <p style="margin: 0; font-size: 0.95rem; opacity: 0.85;">{task['description']}</p>
                <div style="margin-top: 10px; font-size: 0.8rem; opacity: 0.7;">
                    ⏳ Deadline: {format_date(task.get('deadline'))} | 
                    📅 Created: {task.get('created_at', '').split('T')[0]} | 
                    Status: <strong>{task['status']}</strong>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Action Buttons Layout for each card
        col_act1, col_act2, col_act3, col_act4, _ = st.columns([1.5, 1.2, 1.2, 1.2, 6])
        
        # Action behavior based on task status
        if task["status"] == "Deleted":
            with col_act1:
                if st.button("🔄 Restore", key=f"restore_{task_id}"):
                    if restore_task(task_id):
                        st.success("Task restored!")
                        st.rerun()
        else:
            # Complete / Reopen Toggles
            with col_act1:
                if task["status"] == "Completed":
                    if st.button("🔓 Reopen", key=f"reopen_{task_id}"):
                        if toggle_task_status(task_id, to_complete=False):
                            st.rerun()
                else:
                    if st.button("✅ Complete", key=f"complete_{task_id}"):
                        if toggle_task_status(task_id, to_complete=True):
                            st.rerun()
            
            # Edit Option
            with col_act2:
                if st.button("✏️ Edit", key=f"edit_{task_id}"):
                    st.session_state.editing_task_id = task_id
                    st.rerun()
            
            # Delete Option
            with col_act3:
                if st.button("🗑️ Delete", key=f"delete_{task_id}"):
                    if delete_task(task_id):
                        st.success("Task soft-deleted!")
                        st.rerun()

# -----------------
# 5. Bulk Options Section
# -----------------
st.markdown("---")
st.subheader("🧹 Bulk Utilities & Export")
bulk_col1, bulk_col2, bulk_col3 = st.columns([2, 2, 4])

with bulk_col1:
    if st.button("🧹 Clear Completed Tasks"):
        count = clear_completed_tasks()
        if count > 0:
            st.success(f"Successfully cleared {count} completed tasks.")
            st.rerun()
        else:
            st.info("No completed tasks to clear.")

with bulk_col2:
    # Prepare download resource
    json_data = to_json_string(all_tasks)
    st.download_button(
        label="📥 Download Tasks as JSON",
        data=json_data,
        file_name=f"smarttodo_tasks_{datetime.now().strftime('%Y%m%d')}.json",
        mime="application/json"
    )
