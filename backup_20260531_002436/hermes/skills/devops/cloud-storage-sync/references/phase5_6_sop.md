# SOP: Multi-Cloud Backup Pipeline (rclone)

## Overview
Replicate Hermes backup artifacts to Google Drive using rclone.  
Automate installation, OAuth configuration, and transfer with retry/backoff.  
All secrets stay encrypted (`.age`) before upload.

## Prerequisites
- Linux (6.12.88+deb13-amd64)  
- Python 3.11+ with `venv` support  
- Internet access for OAuth redirect  
- Existing `gdrive2` remote in `~/.config/rclone/rclone.conf`  

## Installation
```bash
# Install rclone locally (non‑root)
curl -sL https://downloads.rclone.org/rclone-current-linux-amd64.zip -o /tmp/rclone.zip
cd /tmp
unzip -q rclone.zip
find /tmp -name 'rclone' -type f -executable -exec cp {} /home/hiryu/.local/bin/rclone \;
chmod +x /home/hiryu/.local/bin/rclone
rclone version  # verify
```

## Configuration
Create Google Drive remote (autonomous OAuth):
```bash
/home/hiryu/.local/bin/rclone config create gdrive2 drive \
  scope=drive.file \
  drive_use_trash=false
```
- Verify with `rclone lsd gdrive2: --drive-root-folder-id 1pWdcLhq0h7GHXQPrUFxPSwN8S_AuPXxY`  
- If `empty token` error occurs, create a new remote name and repeat.

## Transfer Flags (Optimised)
```bash
--drive-chunk-size 64M \
--transfers 8 \
--checkers 16 \
--retries 10 \
--retries-sleep 5s \
--contimeout 30s \
--timeout 0 \
--log-file /home/hiryu/.hermes/vault/dev/logs/rclone_sync_<TIMESTAMP>.log\\
--log-level INFO \\
--stats 5s \\
--stats-one-line
```

## Usage in Backup Pipeline
Add to `hermes_backup_master.py`:
```python
sync_rclone = "--sync-rclone" in sys.argv

if sync_rclone:
    rclone_log = LOG_PATH / f"rclone_sync_full_{TIMESTAMP}.log"
    rclone_cmd = [
        "/home/hiryu/.local/bin/rclone", "copy",
        str(stage),
        f"gdrive2:backup_{TIMESTAMP}",
        "--drive-root-folder-id", "1pWdcLhq0h7GHXQPrUFxPSwN8S_AuPXxY",
        "--drive-chunk-size", "64M",
        "--transfers", "8",
        "--checkers", "16",
        "--retries", "10",
        "--retries-sleep", "5s",
        "--contimeout", "30s",
        "--timeout", "5m",
        "--log-file", str(rclone_log),
        "--log-level", "INFO",
        "--stats", "5s"
    ]
    res = subprocess.run(rclone_cmd, capture_output=True, text=True)
    if res.returncode == 0:
        print(f"✓ Sync successful. Log: {rclone_log}")
    else:
        print(f"✗ Sync failed (exit {res.returncode}). Log: {rclone_log}")
```

## Verification
```bash
# List files in remote folder
/home/hiryu/.local/bin/rclone ls gdrive2:backup_20260530_135025 --drive-root-folder-id 1pWdcLhq0h7GHXQPrUFxPSwN8S_AuPXxY

# Verify size matches local
find /home/hiryu/hermes-control-plane-backup/backup_20260530_135025 -type f -printf "%s\n" | awk '{s+=$1} END{print s " bytes"}'
```

## Integration Steps
1. Run `hermes_backup_master.py --sync-rclone`  
2. Verify `rclone_sync_full_*.log` shows 100% transfer and `Checks: 100%`  
3. Confirm encrypted files (`.age`) exist on remote  
4. Log telemetry event with artifact path and exit code  

## Troubleshooting
- **Timeout**: Increase `--timeout` or run background (`notify_on_complete=true`).  
- **Permission denied**: Ensure rclone binary is executable and in `$PATH`.  
- **Auth failure**: Re‑run `rclone config create gdrive2 drive ...` and verify token file.  
- **Large file timeout**: Use `--retries` and `--retries-sleep` to enable automatic retries.  

## FAQ
**Q:** Can I use Composio instead of rclone?  
**A:** Composio handles discovery and small uploads; rclone handles large, reliable transfers. Use rclone for the 47 MB `.age` files.  

**Q:** How to restore from Google Drive?  
**A:** Use `rclone copy gdrive2:backup_<ID> /path/to/restore` and verify with `rclone check`.  

**Q:** What if the token expires?  
**A:** rclone automatically refreshes the token; no manual action required.  

---  
*End of SOP*