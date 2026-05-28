#!/usr/bin/env python3
"""Detached dashboard launcher."""
import subprocess, os, sys

log_path = "/home/hiryu/.hermes/vault/dev/dashboard.log"
os.makedirs(os.path.dirname(log_path), exist_ok=True)

cmd = [
    "/home/hiryu/.hermes/venv/bin/python",
    "-m", "uvicorn",
    "dashboard_api:app",
    "--host", "0.0.0.0",
    "--port", "8000",
]

with open(log_path, "a") as log:
    log.write("=== Launching Dashboard Server ===\n")
    proc = subprocess.Popen(
        cmd + ["--workers", "1"], # Limit to 1 worker to conserve CPU
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        cwd="/home/hiryu/.hermes",
        start_new_session=True,
        close_fds=True,
    )
    log.write(f"PID: {proc.pid}\n")

print(f"launched_pid={proc.pid}")
