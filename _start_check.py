import subprocess, sys, os

env = os.environ.copy()
env["PYTHONPATH"] = r"d:\Third year Projects\Agentverse"

proc = subprocess.run(
    [sys.executable, "-m", "uvicorn", "backend.main:app",
     "--host", "0.0.0.0", "--port", "8000", "--timeout-keep-alive", "5"],
    cwd=r"d:\Third year Projects\Agentverse",
    env=env,
    capture_output=True,
    text=True,
    timeout=15,
)
print("STDOUT:", proc.stdout[-3000:] if proc.stdout else "(none)")
print("STDERR:", proc.stderr[-3000:] if proc.stderr else "(none)")
