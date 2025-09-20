import json, os
from pathlib import Path
from dataclasses import dataclass, asdict
from datetime import datetime

def _db_dir():
    return Path(os.environ.get("CLI_TODO_DB_DIR", Path.home() / ".cli_todo"))

def _db_path():
    return _db_dir() / "todo.json"

@dataclass
class Task:
    id: int
    description: str
    completed: bool = False
    created_at: str = ""
    completed_at: str = ""

def load_tasks():
    path = _db_path()
    if not path.exists():
        return []
    return [Task(**t) for t in json.loads(path.read_text())]

def save_tasks(tasks):
    _db_dir().mkdir(parents=True, exist_ok=True)
    (_db_path()).write_text(json.dumps([asdict(t) for t in tasks], indent=2))

def add_task(desc):
    tasks = load_tasks()
    new_id = max([t.id for t in tasks], default=0) + 1
    task = Task(new_id, desc, False, datetime.utcnow().isoformat(), "")
    tasks.append(task)
    save_tasks(tasks)
    return task

def list_tasks(include_completed=False, only_completed=False):
    tasks = load_tasks()
    if only_completed:
        return [t for t in tasks if t.completed]
    if include_completed:
        return tasks
    return [t for t in tasks if not t.completed]


def complete_task(task_id):
    tasks = load_tasks()
    for t in tasks:
        if t.id == task_id and not t.completed:
            t.completed = True
            t.completed_at = datetime.utcnow().isoformat()
            save_tasks(tasks)
            return True
    return False

def reopen_task(task_id: int) -> bool:
    """Mark a completed task back to active. Return True if changed, else False."""
    tasks = load_tasks()
    changed = False
    for t in tasks:
        if t.id == task_id:
            if t.completed:
                t.completed = False
                t.completed_at = ""
                save_tasks(tasks)
                changed = True
            break
    return changed

def clear_completed():
    tasks = load_tasks()
    keep = [t for t in tasks if not t.completed]
    removed = len(tasks) - len(keep)
    save_tasks(keep)
    return removed
