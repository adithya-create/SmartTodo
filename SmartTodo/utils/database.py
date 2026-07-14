import os
import json
import shutil
import tempfile
import threading
from datetime import datetime
from typing import List, Dict, Any

# Thread lock to prevent race conditions during writes from concurrent users/sessions
_db_lock = threading.Lock()

def get_db_path(filename: str) -> str:
    """
    Get the absolute path to a database file under the database folder.
    Ensures that the directory is created if it does not exist.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_dir = os.path.join(base_dir, "database")
    os.makedirs(db_dir, exist_ok=True)
    return os.path.join(db_dir, filename)

def backup_corrupted_file(file_path: str) -> None:
    """
    Backs up a corrupted database file by renaming it with a timestamp
    so user data is not completely lost during recovery.
    """
    try:
        if os.path.exists(file_path):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = f"{file_path}.corrupted.{timestamp}"
            shutil.move(file_path, backup_path)
    except Exception:
        # Fallback to delete if move fails, preventing application freeze
        try:
            os.remove(file_path)
        except Exception:
            pass

def initialize_db() -> None:
    """
    Ensures both tasks.json and history.json exist.
    If a file is empty or corrupted, it backs up the file (if corrupted)
    and initializes it to a valid empty list.
    """
    for filename in ["tasks.json", "history.json"]:
        path = get_db_path(filename)
        if not os.path.exists(path):
            try:
                with open(path, "w", encoding="utf-8") as f:
                    json.dump([], f, indent=4)
            except Exception:
                pass
        else:
            # Check for corruption or empty contents
            should_reinit = False
            try:
                if os.path.getsize(path) == 0:
                    should_reinit = True
                else:
                    with open(path, "r", encoding="utf-8") as f:
                        content = f.read().strip()
                        if not content:
                            should_reinit = True
                        else:
                            json.loads(content)
            except (json.JSONDecodeError, ValueError, Exception):
                backup_corrupted_file(path)
                should_reinit = True

            if should_reinit:
                try:
                    with open(path, "w", encoding="utf-8") as f:
                        json.dump([], f, indent=4)
                except Exception:
                    pass

def load_json(file_path: str) -> List[Dict[str, Any]]:
    """
    Loads JSON data from the specified path.
    If the file is corrupted, runs recovery to back it up and return an empty list.
    """
    initialize_db()
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError, PermissionError):
        backup_corrupted_file(file_path)
        # Attempt to write a clean empty list
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump([], f, indent=4)
        except Exception:
            pass
        return []
    except Exception:
        return []

def save_json(file_path: str, data: List[Dict[str, Any]]) -> bool:
    """
    Saves a list of dictionaries to a JSON file atomically using a temp file.
    Uses threading locks to ensure thread safety across concurrent sessions.
    """
    initialize_db()
    with _db_lock:
        temp_fd = None
        temp_path = None
        try:
            dir_name = os.path.dirname(file_path)
            # Create temp file in the same directory to ensure atomic os.replace works
            temp_fd, temp_path = tempfile.mkstemp(dir=dir_name, suffix=".tmp")
            with os.fdopen(temp_fd, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            # Replace target file atomically
            os.replace(temp_path, file_path)
            return True
        except Exception:
            # Clean up temp file on failure
            if temp_path and os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except Exception:
                    pass
            return False
