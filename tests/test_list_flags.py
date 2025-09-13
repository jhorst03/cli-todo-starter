import os, sys, tempfile, subprocess
from cli_todo import core

def _run_cli(*args, env=None):
    cmd = [sys.executable, "-m", "cli_todo.cli", *args]
    return subprocess.run(cmd, capture_output=True, text=True, env=env)

def test_list_filters_and_json_output():
    with tempfile.TemporaryDirectory() as tmp:
        env = os.environ.copy()
        env["CLI_TODO_DB_DIR"] = tmp

        # create two tasks (ids 1,2), then complete id 1
        core.add_task("Task A")
        core.add_task("Task B")
        assert core.complete_task(1)

        # default list: only active -> should show Task B
        p = _run_cli("list", env=env)
        assert p.returncode == 0
        assert "Task B" in p.stdout
        assert "Task A" not in p.stdout

        # --completed: only completed -> Task A
        p = _run_cli("list", "--completed", env=env)
        assert p.returncode == 0
        assert "Task A" in p.stdout
        assert "Task B" not in p.stdout

        # --all: both -> A and B
        p = _run_cli("list", "--all", env=env)
        assert p.returncode == 0
        assert "Task A" in p.stdout and "Task B" in p.stdout

        # --format json with --completed filter
        p = _run_cli("list", "--completed", "--format", "json", env=env)
        assert p.returncode == 0
        assert p.stdout.strip().startswith("[")
        assert "Task A" in p.stdout
        assert "Task B" not in p.stdout
