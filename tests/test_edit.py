import os, sys, tempfile, subprocess
from cli_todo import core

def _run_cli(*args, env=None):
    cmd = [sys.executable, "-m", "cli_todo.cli", *args]
    return subprocess.run(cmd, capture_output=True, text=True, env=env)

def test_edit_happy_and_error_paths():
    with tempfile.TemporaryDirectory() as tmp:
        env = os.environ.copy()
        env["CLI_TODO_DB_DIR"] = tmp

        # create two tasks; ids: 1, 2
        core.add_task("Fix bug")
        core.add_task("Write docs")

        # happy path: edit id 2
        p = _run_cli("edit", "2", "Write detailed docs", env=env)
        assert p.returncode == 0
        # list should now reflect edited description
        l = _run_cli("list", env=env)
        assert "Write detailed docs" in l.stdout
        assert "Write docs" not in l.stdout

        # error path: invalid id
        p = _run_cli("edit", "999", "Ghost task", env=env)
        assert p.returncode != 0
        assert (p.stderr or p.stdout).lower().find("no task") != -1
