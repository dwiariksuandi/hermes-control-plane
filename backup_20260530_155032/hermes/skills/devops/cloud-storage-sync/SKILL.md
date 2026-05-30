---
name: cloud-storage-sync
description: >-
  Reliably replicate files/directories to cloud storage (Google Drive, S3, etc.)
  using rclone. Covers non-root installation, OAuth configuration (autonomous),
  optimised transfer flags for slow connections, background sync patterns,
  integrity verification, and integration with the age-encrypted backup pipeline.
tags: [rclone, backup, gdrive, s3, cloud, replication, sync, age]
---

## Trigger

When you need to synchronise files or backup archives to a cloud storage provider, especially when:
- The files are large (>10 MB) and may time out in other wrappers (e.g. `hermes chat` with Composio).
- You need a robust, resumable, and verifiable transfer method.
- The primary task is autonomous replication without user OAuth intervention.
- You are integrating cloud replication into an existing backup pipeline (age-encrypted secrets, state snapshots).

## Role Separation (Composio vs rclone)

| Tool     | Role                        | Strengths                                      |
|----------|-----------------------------|------------------------------------------------|
| Composio | MCP eyes (discovery, small ops) | SaaS tool discovery, metadata, <5 MB uploads |
| rclone   | Workhorse (data movement)       | Large file transfers, retry, checksum, resume   |

**Rule of thumb:** Use Composio MCP to identify/verify remote state. Use rclone to actually move bytes. Never channel large binary uploads through `hermes chat` wrappers — they hit timeout walls.

---

## 1. Installation (Non-Root, Autonomous)

If `rclone version` fails, install locally to avoid `sudo` prompts.

```bash
curl -sL https://downloads.rclone.org/rclone-current-linux-amd64.zip \
  -o /tmp/rclone.zip
cd /tmp && unzip -q rclone.zip
# The binary lives in a versioned subdirectory; use find to locate it
find /tmp -name 'rclone' -type f -executable \
  -exec cp {} /home/hiryu/.local/bin/rclone \;
chmod +x /home/hiryu/.local/bin/rclone
```

**Verification:**
```bash
/home/hiryu/.local/bin/rclone version
# Expected: rclone v1.74.2+ (exit 0)
```

**Pitfall:** The `find` command may hit `Permission denied` on `/tmp/systemd-private-*` dirs. Ignore those — they don't affect the copy. If the `find` approach is unreliable, pipe to `head -1` or use a direct known path after inspecting the extracted tree.

---

## 2. Configuration — Google Drive OAuth (Fully Autonomous)

**Important finding:** `rclone config create` with the `drive` backend **does** work autonomously. It opens a local HTTP server (port 53682), captures the OAuth redirect, and writes the token to the config file. The output goes to stdout as JSON.

**Do NOT use `rclone config reconnect`** — that requires interactive terminal input (y/n prompts) and hangs in non-interactive environments.

**Correct autonomous approach:**

```bash
# Creates the remote, starts local OAuth server, captures token, writes config
# The --drive-root-folder-id flag is optional but recommended
/home/hiryu/.local/bin/rclone config create <remote-name> drive \
  scope=drive.file \
  drive_use_trash=false
```

- If this is a brand new environment (no cached OAuth from previous browser sessions), the command will output a token on success.
- If the environment has a cached browser session or the command hangs, use the alternative `--non-interactive` flag to create the skeleton first, then rely on the refresh token flow.

**Verification (read-only health check):**
```bash
# List files at the root of a specific folder (exit 0 = auth works)
/home/hiryu/.local/bin/rclone ls <remote-name>: \
  --drive-root-folder-id <folder-id>
```

**Config file location:** `/home/hiryu/.config/rclone/rclone.conf`
- Contains the OAuth token as JSON inside the remote section.
- Token includes `access_token`, `refresh_token`, `expiry`.

**Pitfalls:**
- The `config create` command starts a local HTTP server. If you are on a headless VM with no browser, the redirect may still work because Google sends the token to the redirect URL. rclone handles this internally.
- If you see `CRITICAL: empty token found`, do NOT run `reconnect`. Instead, create a fresh remote with a new name.
- The token in stdout is partially redacted by rclone (`ya29.a...0206`); the full token is written to the config file.
- The `team_drive =` field in the output is normal (empty = not a shared drive).

---

## 3. Transfer Flags (Optimised for Slow/Limited Connections)

Default rclone transfer parameters assume fast connections. On VMs with rate-limited Google Drive API access (~3-4 KiB/s), use these flags:

```bash
# Core flags
--drive-chunk-size 64M     # Larger chunks = fewer API calls
--transfers 8              # Concurrent transfers
--checkers 16              # Parallel file checking

# Reliability flags
--retries 10               # Retries on transient API errors
--retries-sleep 5s         # Backoff between retries
--contimeout 30s           # Connection timeout
--timeout 0                # No timeout (wait indefinitely)

# Logging and progress
--log-file /path/to/sync.log
--log-level INFO
--stats 5s                 # Progress update interval
--stats-one-line           # Compact progress line
```

**Full command for large (>10 MB) transfers:**
```bash
SOURCE_DIR=/home/hiryu/hermes-control-plane-backup/backup_<ID>
DEST_PATH=<remote-name>:backup_<ID>

/home/hiryu/.local/bin/rclone copy \
  "$SOURCE_DIR" "$DEST_PATH" \
  --drive-root-folder-id <folder-id> \
  --drive-chunk-size 64M \
  --transfers 8 \
  --checkers 16 \
  --retries 10 \
  --retries-sleep 5s \
  --contimeout 30s \
  --timeout 0 \
  --log-file /home/hiryu/.hermes/vault/dev/logs/rclone_sync_<DATE>.log \
  --log-level INFO \
  --stats 5s
```

---

## 4. Background Sync (Very Slow Connections)

When transfer speed is very low (~3-4 KiB/s, ETA >30 min), run the copy in the background and poll for completion.

```bash
# Start in background via terminal() with notify_on_complete=true
# Use --timeout 0 so it doesn't get killed mid-transfer
terminal(command="rclone copy ... --timeout 0", background=true, notify_on_complete=true)
```

Then poll or wait:
```bash
# Check progress
tail -n 5 /path/to/rclone_sync*.log

# Or wait for process
process(action="wait", session_id="...")
```

**Pitfall:** If `--timeout 0` is not recognised (older rclone versions), use `--timeout 0s` instead.

---

## 5. Integrity Verification

After upload completes, verify byte-for-byte consistency:

```bash
/home/hiryu/.local/bin/rclone check \
  "$SOURCE_DIR" "$DEST_PATH" \
  --drive-root-folder-id <folder-id>
```

Exit code 0 = all files match. Non-zero = discrepancies logged to stderr.

If `rclone check` is unavailable or too slow, use size-based verification:
```bash
# List remote with sizes
rclone lsf "$DEST_PATH" --drive-root-folder-id <folder-id> --format "sp"

# Compare locally
du -sb "$SOURCE_DIR"/* | sort -k2
```

---

## 6. Backup Pipeline Integration

Incorporate rclone sync into the existing backup pipeline (e.g. `hermes_backup_master.py`):

```python
import subprocess

def cloud_sync(source_dir, remote_name, remote_path, folder_id, log_path):
    """Sync a backup directory to cloud storage via rclone."""
    cmd = [
        str(backup_tool), "copy",
        str(source_dir),
        f"{remote_name}:{remote_path}",
        "--drive-root-folder-id", folder_id,
        "--drive-chunk-size", "64M",
        "--transfers", "8",
        "--checkers", "16",
        "--retries", "10",
        "--retries-sleep", "5s",
        "--contimeout", "30s",
        "--timeout", "0",
        "--log-file", str(log_path),
        "--log-level", "INFO",
        "--stats", "5s",
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    return r.returncode == 0
```

**Pipeline sequence:**
1. Run `hermes_backup_master.py` (generates backup directory, encrypted secrets, manifest)
2. Call `cloud_sync()` for the latest backup directory
3. Run `rclone check` for verification
4. Log telemetry event with artifact path and exit code

---

## References

See `references/gdrive-rate-limit-patterns.md` for real session output, timeout diagnostics, and flag-tuning decisions.

## Evidence Checklist

After each sync:
- [ ] `rclone copy` exit code 0
- [ ] Remote listing matches local (rclone check)
- [ ] `.age` files present on remote
- [ ] Log file written
- [ ] Telemetry event logged
