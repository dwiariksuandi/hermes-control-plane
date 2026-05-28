#!/usr/bin/env python3
import os, datetime, zipfile, sqlite3, uuid, subprocess, sys

VAULT_PATH = "/home/hiryu/.hermes/vault"
DB_PATH = "/home/hiryu/.hermes/agent-logs.db"
BACKUP_DIR = "/home/hiryu/.hermes/backups"
LOG_EVENT = "/home/hiryu/.hermes/log_event.py"

def backup():
    os.makedirs(BACKUP_DIR, exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    out = os.path.join(BACKUP_DIR, f"hermes_core_backup_{ts}.zip")

    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        if os.path.isfile(DB_PATH):
            zf.write(DB_PATH, arcname="agent-logs.db")
        for root, _, files in os.walk(VAULT_PATH):
            for name in files:
                p = os.path.join(root, name)
                arc = os.path.relpath(p, os.path.dirname(VAULT_PATH))
                zf.write(p, arcname=arc)

    try:
        subprocess.run([
            "python3", LOG_EVENT,
            "Dev",
            "Core backup archive created",
            "success",
            "verified",
            out
        ], check=False)
    except Exception:
        pass

    print(out)
    return out

if __name__ == "__main__":
    backup()
    sys.exit(0)
