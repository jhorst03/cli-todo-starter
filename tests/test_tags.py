import os, sys, tempfile, subprocess
from cli_todo import core

def _run_cli(*args, env=None):
    cmd = [sys.executable, "-m", "cli_todo.cli", *args]
    return subprocess.run(cmd, capture_output=True, text=True, env=env)

def test_add_with_tags_and_list_filter_by_tag():
    with tempfile.TemporaryDirectory() as tmp:
        env = os.environ.copy()
        env["CLI_TODO_DB_DIR"] = tmp

        # Add tasks with and without tags
        p = _run_cli("add", "Write docs", "--tags", "work,docs", env=env); assert p.returncode == 0
        p = _run_cli("add", "Buy milk", env=env); assert p.returncode == 0
        p = _run_cli("add", "Fix login", "--tags", "work,bug", env=env); assert p.returncode == 0

        # Filter by 'work' (should include Write docs, Fix login; exclude Buy milk)
        p = _run_cli("list", "--tag", "work", env=env)
        assert p.returncode == 0
        out = p.stdout
        assert "Write docs" in out and "Fix login" in out
        assert "Buy milk" not in out

        # JSON output with tag filter
        p = _run_cli("list", "--tag", "docs", "--format", "json", env=env)
        assert p.returncode == 0
        assert p.stdout.strip().startswith("[")
        assert "Write docs" in p.stdout
        assert "Fix login" not in p.stdout

        # Ensure tags are persisted in JSON
        assert '"tags":' in p.stdout
