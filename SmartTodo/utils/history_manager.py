import uuid
from datetime import datetime
from typing import List, Dict, Any
from utils.database import get_db_path, load_json, save_json

def get_history_path() -> str:
    """Retrieve the absolute database path for history logs."""
    return get_db_path("history.json")

def log_action(
    action: str,
    task_id: str,
    task_title: str,
    description: str,
    prev_status: str | None,
    curr_status: str
) -> None:
    """
    Appends an operational log to history.json.
    Ensures that logging errors do not crash the parent transaction.
    Logs are prepended so that they are ordered from newest to oldest by default.
    """
    try:
        path = get_history_path()
        logs = load_json(path)
        
        new_log = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "task_id": task_id,
            "task_title": task_title,
            "description": description,
            "previous_status": prev_status,
            "current_status": curr_status
        }
        
        logs.insert(0, new_log)
        save_json(path, logs)
    except Exception:
        # Gracefully handle database or write locks to not crash main interface actions
        pass

def get_history() -> List[Dict[str, Any]]:
    """Retrieves all logs from the audit database."""
    try:
        path = get_history_path()
        return load_json(path)
    except Exception:
        return []

def clear_history() -> bool:
    """Clears all history log records."""
    try:
        path = get_history_path()
        return save_json(path, [])
    except Exception:
        return False
