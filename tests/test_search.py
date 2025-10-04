import os, sys, tempfile, subprocess
from cli_todo import core

def _run_cli(*args, env=None):
    cmd = [sys.executable, "-m", "cli_todo.cli", *args]
    return subprocess.run(cmd, capture_output=True, text=True, env=env)

def test_search_command():
    with tempfile.TemporaryDirectory() as tmp:
        env = os.environ.copy()
        env["CLI_TODO_DB_DIR"] = tmp

        core.add_task("Fix login bug")
        core.add_task("Write documentation")
        core.add_task("Review codebase")

        # Case-insensitive match
        p = _run_cli("search", "fix", env=env)
        assert p.returncode == 0
        assert "Fix login bug" in p.stdout

        # Another match
        p = _run_cli("search", "code", env=env)
        assert p.returncode == 0
        assert "Review codebase" in p.stdout

        # No match
        p = _run_cli("search", "database", env=env)
        assert p.returncode == 0
        assert "No results found" in p.stdout
