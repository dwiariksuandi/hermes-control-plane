"""Aegis Janitor — vault entropy cure + secret sweep."""

from __future__ import annotations

import os
import time
import subprocess
from pathlib import Path
from typing import Dict, List, Any


def cure_entropy(vault_path: str, days_old: int = 3) -> Dict[str, Any]:
    """Delete stale hygiene targets in vault.

    Targets:
    - *.bak
    - dummy_*
    - *_temp

    Only deletes files older than days_old.
    """
    root = Path(vault_path).resolve()
    if not root.exists() or not root.is_dir():
        raise ValueError(f"Invalid vault_path: {root}")

    cutoff = time.time() - (days_old * 86400)
    deleted: List[str] = []
    skipped: List[str] = []

    patterns = ["*.bak", "*.bak.*", "dummy_*", "*_temp"]

    for pattern in patterns:
        for p in root.rglob(pattern):
            if not p.is_file():
                continue
            try:
                mtime = p.stat().st_mtime
                if mtime < cutoff:
                    p.unlink()
                    deleted.append(str(p))
                else:
                    skipped.append(str(p))
            except Exception:
                skipped.append(str(p))

    return {
        "vault_path": str(root),
        "days_old": days_old,
        "deleted_count": len(deleted),
        "deleted": deleted,
        "skipped_count": len(skipped),
    }


def sweep_secrets(vault_path: str) -> Dict[str, Any]:
    """Run trufflehog filesystem scan and capture findings."""
    root = Path(vault_path).resolve()
    if not root.exists() or not root.is_dir():
        raise ValueError(f"Invalid vault_path: {root}")

    cmd = ["trufflehog", "filesystem", str(root)]

    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=600,
            check=False,
        )
        output = (proc.stdout or "") + ("\n" + proc.stderr if proc.stderr else "")
        # Heuristic: if output contains findings markers, flag detected.
        secrets_detected = any(k in output.lower() for k in ["found", "verified", "detector"]) and proc.returncode != 127
        return {
            "command": " ".join(cmd),
            "return_code": proc.returncode,
            "secrets_detected": bool(secrets_detected),
            "output": output.strip(),
        }
    except FileNotFoundError:
        return {
            "command": " ".join(cmd),
            "return_code": 127,
            "secrets_detected": False,
            "output": "trufflehog binary not found in PATH",
        }
    except subprocess.TimeoutExpired:
        return {
            "command": " ".join(cmd),
            "return_code": 124,
            "secrets_detected": False,
            "output": "trufflehog scan timed out",
        }


def run_maintenance(vault_path: str = "/home/hiryu/.hermes/vault", days_old: int = 3) -> Dict[str, Any]:
    """Run entropy cleanup then secret sweep."""
    entropy = cure_entropy(vault_path=vault_path, days_old=days_old)
    secrets = sweep_secrets(vault_path=vault_path)
    return {
        "status": "ok",
        "entropy": entropy,
        "secrets": secrets,
    }


if __name__ == "__main__":
    result = run_maintenance()
    print(result)
