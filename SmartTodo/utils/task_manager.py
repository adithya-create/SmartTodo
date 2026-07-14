import uuid
from datetime import datetime
from typing import List, Dict, Any
from utils.database import get_db_path, load_json, save_json
from utils.history_manager import log_action

def get_tasks_path() -> str:
    """Gets the absolute database path for tasks."""
    return get_db_path("tasks.json")

def get_all_tasks() -> List[Dict[str, Any]]:
    """Retrieves all tasks stored in the database."""
    try:
        path = get_tasks_path()
        return load_json(path)
    except Exception:
        return []

def create_task(
    title: str,
    description: str,
    priority: str,
    category: str,
    deadline: str | None
) -> Dict[str, Any] | None:
    """
    Creates a new task, stores it in database/tasks.json,
    and logs the creation event in history.
    """
    try:
        path = get_tasks_path()
        tasks = load_json(path)
        
        now_str = datetime.now().isoformat()
        
        # Ensure deadline is stored cleanly as string
        deadline_str = str(deadline) if deadline else None

        new_task = {
            "id": str(uuid.uuid4()),
            "title": title.strip(),
            "description": description.strip(),
            "priority": priority,
            "category": category,
            "deadline": deadline_str,
            "status": "Pending",
            "created_at": now_str,
            "updated_at": now_str,
            "completed_at": None
        }
        
        tasks.append(new_task)
        if save_json(path, tasks):
            log_action(
                action="Task Created",
                task_id=new_task["id"],
                task_title=new_task["title"],
                description=new_task["description"],
                prev_status=None,
                curr_status="Pending"
            )
            return new_task
        return None
    except Exception:
        return None

def update_task(task_id: str, updates: Dict[str, Any]) -> Dict[str, Any] | None:
    """
    Updates specific attributes of an existing task.
    Sets the updated_at timestamp and logs the update action.
    """
    try:
        path = get_tasks_path()
        tasks = load_json(path)
        
        for task in tasks:
            if task["id"] == task_id:
                prev_status = task["status"]
                
                # Check for allowed update keys to prevent data contamination
                allowed_keys = ["title", "description", "priority", "category", "deadline", "status"]
                for key in allowed_keys:
                    if key in updates:
                        if key == "title" or key == "description":
                            task[key] = updates[key].strip()
                        else:
                            task[key] = updates[key]
                
                task["updated_at"] = datetime.now().isoformat()
                
                # Handle status changes side-effects
                if "status" in updates:
                    curr_status = updates["status"]
                    if curr_status == "Completed" and prev_status != "Completed":
                        task["completed_at"] = datetime.now().isoformat()
                    elif curr_status == "Pending":
                        task["completed_at"] = None
                
                if save_json(path, tasks):
                    log_action(
                        action="Task Updated",
                        task_id=task["id"],
                        task_title=task["title"],
                        description=task["description"],
                        prev_status=prev_status,
                        curr_status=task["status"]
                    )
                    return task
                break
        return None
    except Exception:
        return None

def delete_task(task_id: str) -> bool:
    """
    Performs a soft delete of a task by changing its status to 'Deleted'.
    This allows for restoring tasks.
    """
    try:
        path = get_tasks_path()
        tasks = load_json(path)
        
        for task in tasks:
            if task["id"] == task_id:
                prev_status = task["status"]
                if prev_status == "Deleted":
                    return True # already deleted
                
                task["status"] = "Deleted"
                task["updated_at"] = datetime.now().isoformat()
                
                if save_json(path, tasks):
                    log_action(
                        action="Task Deleted",
                        task_id=task["id"],
                        task_title=task["title"],
                        description=task["description"],
                        prev_status=prev_status,
                        curr_status="Deleted"
                    )
                    return True
                break
        return False
    except Exception:
        return False

def restore_task(task_id: str) -> bool:
    """
    Restores a soft-deleted task back to 'Pending' status.
    """
    try:
        path = get_tasks_path()
        tasks = load_json(path)
        
        for task in tasks:
            if task["id"] == task_id:
                prev_status = task["status"]
                if prev_status != "Deleted":
                    return True # not deleted
                
                task["status"] = "Pending"
                task["updated_at"] = datetime.now().isoformat()
                task["completed_at"] = None
                
                if save_json(path, tasks):
                    log_action(
                        action="Task Restored",
                        task_id=task["id"],
                        task_title=task["title"],
                        description=task["description"],
                        prev_status=prev_status,
                        curr_status="Pending"
                    )
                    return True
                break
        return False
    except Exception:
        return False

def toggle_task_status(task_id: str, to_complete: bool) -> bool:
    """
    Helper function to toggle a task status between 'Completed' and 'Pending'.
    """
    try:
        path = get_tasks_path()
        tasks = load_json(path)
        
        for task in tasks:
            if task["id"] == task_id:
                prev_status = task["status"]
                new_status = "Completed" if to_complete else "Pending"
                
                if prev_status == new_status:
                    return True
                
                task["status"] = new_status
                task["updated_at"] = datetime.now().isoformat()
                
                if to_complete:
                    task["completed_at"] = datetime.now().isoformat()
                    action_name = "Task Completed"
                else:
                    task["completed_at"] = None
                    action_name = "Task Reopened"
                
                if save_json(path, tasks):
                    log_action(
                        action=action_name,
                        task_id=task["id"],
                        task_title=task["title"],
                        description=task["description"],
                        prev_status=prev_status,
                        curr_status=new_status
                    )
                    return True
                break
        return False
    except Exception:
        return False

def clear_completed_tasks() -> int:
    """
    Permanently removes all tasks marked as 'Completed'.
    Returns the count of tasks cleared.
    """
    try:
        path = get_tasks_path()
        tasks = load_json(path)
        
        original_count = len(tasks)
        # Filter out completed tasks
        remaining_tasks = [t for t in tasks if t["status"] != "Completed"]
        cleared_count = original_count - len(remaining_tasks)
        
        if cleared_count > 0:
            if save_json(path, remaining_tasks):
                log_action(
                    action="Completed Tasks Cleared",
                    task_id="system-clear",
                    task_title="System Action",
                    description=f"Cleared {cleared_count} completed tasks from database.",
                    prev_status="Completed",
                    curr_status="Permanent Delete"
                )
                return cleared_count
        return 0
    except Exception:
        return 0
