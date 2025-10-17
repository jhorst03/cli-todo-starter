import os, sys, tempfile, subprocess
from cli_todo import core

def _run_cli(*args, env=None):
    cmd = [sys.executable, "-m", "cli_todo.cli", *args]
    return subprocess.run(cmd, capture_output=True, text=True, env=env)

def test_stats_text_and_json():
    with tempfile.TemporaryDirectory() as tmp:
        env = os.environ.copy()
        env["CLI_TODO_DB_DIR"] = tmp

        # No tasks -> totals 0
        p = _run_cli("stats", env=env)
        assert p.returncode == 0
        assert "total: 0" in p.stdout.lower()

        # Add two, complete one
        core.add_task("Write tests")      # id 1
        core.add_task("Fix bug")          # id 2
        assert core.complete_task(1)

        # Text stats
        p = _run_cli("stats", env=env)
        out = p.stdout.lower()
        assert p.returncode == 0
        assert "total: 2" in out
        assert "active: 1" in out
        assert "completed: 1" in out
        # completion rate should be 0.5 (or 50%)
        assert "0.5" in out or "50%" in out

        # JSON stats
        p = _run_cli("stats", "--format", "json", env=env)
        assert p.returncode == 0
        assert p.stdout.strip().startswith("{")
        assert '"total": 2' in p.stdout
        assert '"active": 1' in p.stdout
        assert '"completed": 1' in p.stdout
