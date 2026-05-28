#!/usr/bin/env python3
"""Lightweight workspace mapper watcher."""

import time
import subprocess
from pathlib import Path

HERMES = Path("/home/hiryu/.hermes")
WATCH_PATHS = [HERMES, HERMES / "vault"]
MAPPER = HERMES / "workspace_mapper.py"
PYTHON = HERMES / "venv/bin/python"
INTERVAL = 30


def run_mapper():
    try:
        subprocess.run([str(PYTHON), str(MAPPER)], capture_output=True, text=True, check=False, timeout=300)
    except Exception:
        pass


def newest_mtime() -> float:
    latest = 0.0
    for base in WATCH_PATHS:
        for p in base.rglob("*"):
            if not p.is_file() or p.name.startswith('.'):
                continue
            try:
                latest = max(latest, p.stat().st_mtime)
            except (FileNotFoundError, PermissionError):
                continue
    return latest


def main():
    last_seen = newest_mtime()
    while True:
        time.sleep(INTERVAL)
        current = newest_mtime()
        if current > last_seen:
            last_seen = current
            run_mapper()


if __name__ == "__main__":
    main()
