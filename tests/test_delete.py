import os, sys, tempfile, subprocess
from cli_todo import core

def _run_cli(*args, env=None):
    cmd = [sys.executable, "-m", "cli_todo.cli", *args]
    return subprocess.run(cmd, capture_output=True, text=True, env=env)

def test_delete_happy_and_error_paths():
    with tempfile.TemporaryDirectory() as tmp:
        env = os.environ.copy()
        env["CLI_TODO_DB_DIR"] = tmp

        core.add_task("Write docs")   # id 1
        core.add_task("Fix bug")      # id 2

        p = _run_cli("delete", "1", env=env)
        assert p.returncode == 0

        lp = _run_cli("list", env=env);      assert "Write docs" not in lp.stdout
        lj = _run_cli("list", "--format", "json", env=env)
        assert '"Write docs"' not in lj.stdout

        p = _run_cli("delete", "999", env=env)
        assert p.returncode != 0
        assert (p.stderr or p.stdout).lower().find("no task") != -1
