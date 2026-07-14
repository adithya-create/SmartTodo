import os
import sys

# Append parent workspace directory to PYTHONPATH
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.database import get_db_path, load_json, save_json, initialize_db
from utils.task_manager import create_task, update_task, delete_task, restore_task, toggle_task_status, get_all_tasks
from utils.history_manager import get_history, clear_history
from utils.validator import validate_task_input

def run_tests() -> None:
    print("[START] Initializing SmartTodo Verification Suite...")
    
    # Define database directory
    db_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database")
    
    # Temporary backup of existing databases to ensure we don't destroy user data
    backups = {}
    if os.path.exists(db_dir):
        for filename in ["tasks.json", "history.json"]:
            path = os.path.join(db_dir, filename)
            if os.path.exists(path):
                backup_path = path + ".verifybak"
                if os.path.exists(backup_path):
                    os.remove(backup_path)
                os.rename(path, backup_path)
                backups[path] = backup_path
                
    try:
        # Re-initialize clean DB
        initialize_db()
        print("[OK] Database folder and JSON structures initialized.")
        
        # 1. Test Task Creation
        print("Testing task creation...")
        t1 = create_task(
            title="Register for marathon",
            description="Complete the 10k race sign-up page online.",
            priority="High",
            category="Fitness",
            deadline="2029-10-15"
        )
        assert t1 is not None, "Task creation returned None"
        assert t1["title"] == "Register for marathon", "Task title mismatches."
        assert t1["status"] == "Pending", "New task status is not Pending."
        print("[OK] Task creation verified.")
        
        # 2. Test Input Validation (Empty Title, Deadline, Duplicates)
        print("Testing task validation parameters...")
        all_tasks = get_all_tasks()
        
        # Test Empty Title
        is_valid, msg = validate_task_input("", "Fitness", "2029-10-15", all_tasks)
        assert not is_valid, "Blank title should be rejected."
        
        # Test Duplicate check
        is_valid, msg = validate_task_input("Register for marathon", "Fitness", "2029-10-15", all_tasks)
        assert not is_valid, "Duplicate title in same category should be rejected."
        
        is_valid, msg = validate_task_input("Register for marathon", "Work", "2029-10-15", all_tasks)
        assert is_valid, "Same title in a different category should be allowed."
        print("[OK] Input validation verified.")
        
        # 3. Test Task Toggle Completion Status
        print("Testing completion status toggle...")
        t_id = t1["id"]
        status_ok = toggle_task_status(t_id, to_complete=True)
        assert status_ok, "Failed to toggle task to completed."
        
        updated_tasks = get_all_tasks()
        t1_updated = next(t for t in updated_tasks if t["id"] == t_id)
        assert t1_updated["status"] == "Completed", "Task status was not updated to Completed."
        assert t1_updated["completed_at"] is not None, "completed_at field should be set."
        print("[OK] Completion toggle verified.")
        
        # 4. Test History Logs Auditing
        print("Testing history audit logger...")
        logs = get_history()
        assert len(logs) > 0, "No audit history logs were generated."
        actions = [log["action"] for log in logs]
        assert "Task Created" in actions, "Action 'Task Created' missing from logs."
        assert "Task Completed" in actions, "Action 'Task Completed' missing from logs."
        print("[OK] Audit logging verified.")
        
        # 5. Test Soft-Deletion and Restoration Workflow
        print("Testing soft deletion...")
        del_ok = delete_task(t_id)
        assert del_ok, "Task soft-deletion transaction failed."
        
        tasks_post_delete = get_all_tasks()
        t1_deleted = next(t for t in tasks_post_delete if t["id"] == t_id)
        assert t1_deleted["status"] == "Deleted", "Task status was not set to Deleted."
        
        print("Testing restoration workflow...")
        restore_ok = restore_task(t_id)
        assert restore_ok, "Task restoration transaction failed."
        
        tasks_post_restore = get_all_tasks()
        t1_restored = next(t for t in tasks_post_restore if t["id"] == t_id)
        assert t1_restored["status"] == "Pending", "Task status was not reset to Pending."
        print("[OK] Soft deletion and restoration verified.")
        
    finally:
        # Restore backups
        print("Cleaning up verification environment and restoring user databases...")
        for orig, backup in backups.items():
            if os.path.exists(orig):
                os.remove(orig)
            os.rename(backup, orig)
            
    print("\n[SUCCESS] ALL LOGIC AND TRANSACTION TESTS PASSED SUCCESSFULLY! SmartTodo core engine is verified.")

if __name__ == "__main__":
    run_tests()
