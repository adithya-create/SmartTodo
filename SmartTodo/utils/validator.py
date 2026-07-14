import os
from datetime import datetime, date
from typing import List, Dict, Any, Tuple
from utils.database import get_db_path, load_json

def validate_task_input(
    title: str,
    category: str,
    deadline_val: date | str | None,
    existing_tasks: List[Dict[str, Any]],
    edit_task_id: str | None = None
) -> Tuple[bool, str]:
    """
    Validates task fields before creation or update.
    Ensures:
      - Title is not empty or whitespace.
      - Deadline is a valid date and not in the past (for active tasks).
      - Title is unique within the selected category for active tasks (soft deleted tasks are ignored).
    Returns a tuple: (is_valid, error_message).
    """
    # 1. Empty title validation
    if not title or not title.strip():
        return False, "Task title cannot be empty."
    
    # 2. Invalid deadline validation
    if deadline_val:
        try:
            if isinstance(deadline_val, str):
                deadline_date = datetime.strptime(deadline_val, "%Y-%m-%d").date()
            elif isinstance(deadline_val, date):
                deadline_date = deadline_val
            else:
                return False, "Invalid deadline format."
            
            # Deadline should not be in the past
            if deadline_date < date.today():
                return False, "Deadline cannot be in the past."
        except ValueError:
            return False, "Deadline must be a valid date in YYYY-MM-DD format."
            
    # 3. Duplicate task validation (title + category check on non-deleted tasks)
    normalized_title = title.strip().lower()
    normalized_category = category.strip().lower()
    
    for task in existing_tasks:
        # Ignore comparison with itself during edit
        if edit_task_id and task.get("id") == edit_task_id:
            continue
        
        # Only check active/non-deleted tasks
        if task.get("status") != "Deleted":
            t_title = task.get("title", "").strip().lower()
            t_cat = task.get("category", "").strip().lower()
            if t_title == normalized_title and t_cat == normalized_category:
                return False, f"A task with the title '{title.strip()}' already exists in category '{category}'."
                
    return True, ""

def validate_env_setup() -> Tuple[bool, List[str]]:
    """
    Validates whether the environment configuration file .env exists
    and contains all the required configuration keys.
    Returns (is_valid, list_of_errors).
    """
    errors = []
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env_path = os.path.join(base_dir, ".env")
    
    if not os.path.exists(env_path):
        errors.append("Missing .env configuration file in the project root.")
        return False, errors
        
    try:
        from dotenv import load_dotenv
        load_dotenv(env_path)
    except Exception as e:
        errors.append(f"Failed to load environment variables: {str(e)}")
        return False, errors
        
    required_keys = ["APP_NAME", "APP_VERSION", "SECRET_KEY"]
    for key in required_keys:
        val = os.getenv(key)
        if not val or not val.strip():
            errors.append(f"Environment variable '{key}' is missing or empty in .env.")
            
    if errors:
        return False, errors
    return True, []

def check_db_health() -> Tuple[bool, str]:
    """
    Checks if database files are present and can be parsed correctly.
    Returns (is_healthy, status_message).
    """
    tasks_path = get_db_path("tasks.json")
    history_path = get_db_path("history.json")
    
    if not os.path.exists(tasks_path) or not os.path.exists(history_path):
        return False, "Database files do not exist yet. They will be auto-generated."
        
    try:
        tasks = load_json(tasks_path)
        history = load_json(history_path)
        if not isinstance(tasks, list) or not isinstance(history, list):
            return False, "Database format is corrupted. File will be reset on update."
    except Exception as e:
        return False, f"Database health check failed: {str(e)}"
        
    return True, "Database is healthy and verified."
