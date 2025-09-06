import os, sys, tempfile, subprocess

def test_done_invalid_id_exit_code():
    with tempfile.TemporaryDirectory() as tmp:
        env = os.environ.copy()
        env["CLI_TODO_DB_DIR"] = tmp
        proc = subprocess.run(
            [sys.executable, "-m", "cli_todo.cli", "done", "999"],
            env=env,
            capture_output=True,
            text=True,
        )
        # After the fix this must be non-zero and mention "not found"
        assert proc.returncode != 0
        assert "not found" in (proc.stderr or proc.stdout).lower()
