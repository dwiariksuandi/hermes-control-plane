#!/usr/bin/env bash
# Aegis Automation Setup — Cron + Watcher

set -euo pipefail

HERMES_ROOT="/home/hiru/.hermes"
# Fix typo: should be hiryu
HERMES_ROOT="/home/hiryu/.hermes"

# 1. Setup cron job for daily janitor run at 2am
(crontab -l 2>/dev/null; echo "0 2 * * * $HERMES_ROOT/venv/bin/python $HERMES_ROOT/aegis/aegis_janitor.py >> $HERMES_ROOT/vault/dev/janitor.log 2>&1") | crontab -

echo "Cron job installed: daily janitor at 02:00"

# 2. Create lightweight file watcher (polling every 30s) for workspace_mapper.py refresh
WATCHER_SCRIPT="$HERMES_ROOT/aegis/aegis_watcher.py"

cat > "$WATCHER_SCRIPT" <<'PY'
#!/usr/bin/env python3
import time
import subprocess
from pathlib import Path

HERMES = Path("/home/hiryu/.hermes")
WATCH_PATHS = [HERMES, HERMES / "vault"]
MAPPER = HERMES / "workspace_mapper.py"
INTERVAL = 30  # seconds

def run_mapper():
    try:
        subprocess.run([str(HERMES / "venv/bin/python"), str(MAPPER)], 
                       capture_output=True, check=False)
    except Exception:
        pass

def main():
    print("Workspace mapper watcher started (polling every 30s)")
    last_mtime = 0
    while True:
        try:
            # Check if any watched file changed
            changed = False
            for base in WATCH_PATHS:
                for p in base.rglob("*"):
                    if p.is_file() and not p.name.startswith('.'):
                        try:
                            m = p.stat().st_mtime
                            if m > last_mtime:
                                changed = True
                                break
                        except (FileNotFoundError, PermissionError):
                            continue
                if changed:
                    break
            if changed:
                last_mtime = time.time()
                run_mapper()
        except KeyboardInterrupt:
            break
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()
PY

chmod +x "$WATCHER_SCRIPT"
echo "Watcher script created: $WATCHER_SCRIPT"

# 3. Add watcher to cron (runs at reboot)
(crontab -l 2>/dev/null; echo "@reboot $HERMES_ROOT/venv/bin/python $HERMES_ROOT/aegis/aegis_watcher.py >> $HERMES_ROOT/vault/dev/watcher.log 2>&1") | crontab -

echo "Watcher cron job installed (@reboot)"
echo "To start watcher now: $HERMES_ROOT/venv/bin/python $WATCHER_SCRIPT &"