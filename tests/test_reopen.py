import os, sys, tempfile, subprocess
from cli_todo import core

def _run_cli(*args, env=None):
    cmd = [sys.executable, "-m", "cli_todo.cli", *args]
    return subprocess.run(cmd, capture_output=True, text=True, env=env)

def test_reopen_happy_and_error_paths():
    with tempfile.TemporaryDirectory() as tmp:
        env = os.environ.copy()
        env["CLI_TODO_DB_DIR"] = tmp

        # create two tasks; complete id 1
        core.add_task("Fix bug")
        core.add_task("Write docs")
        assert core.complete_task(1)

        # happy: reopen id 1 -> should succeed and make it active again
        p = _run_cli("reopen", "1", env=env)
        assert p.returncode == 0
        # list should contain id 1 as active now
        lp = _run_cli("list", env=env)
        assert "Fix bug" in lp.stdout

        # error: invalid id
        p = _run_cli("reopen", "999", env=env)
        assert p.returncode != 0
        assert (p.stderr or p.stdout).lower().find("no task") != -1

        # error: reopening an already active task (id 1)
        p = _run_cli("reopen", "1", env=env)
        assert p.returncode != 0
        assert (p.stderr or p.stdout).lower().find("already active") != -1
