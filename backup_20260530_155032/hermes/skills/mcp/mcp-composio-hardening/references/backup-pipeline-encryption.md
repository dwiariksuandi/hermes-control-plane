# Backup Pipeline Encryption Integration (Phase 5.3)

## Context
This document records the integration pattern for encrypting secret files within the Hermes backup pipeline (`hermes_backup_master.py`).

## Pipeline Steps (Step 1.5)
After the main copy loop and before manifest writing:

1. Derive public key from private key file:
   ```python
   subprocess.run([AGE_BIN + "-keygen", "-y", AGE_KEY], capture_output=True, text=True)
   ```
   NOTE: use `age-keygen -y` NOT `age -y`. The `age` binary itself does not accept `-y`.

2. For each secret file (.env, auth.json):
   - `age -r PUBKEY -o <dest>.age <src>`
   - `unlink <src>` (remove plaintext from staging)

3. For state.db:
   - Create snapshot via SQLite `.backup()` API
   - Encrypt snapshot
   - Delete snapshot from staging

4. Set permissions:
   - `chmod 700` on encrypted directory
   - `chmod 600` on each `.age` file

5. Exclude `hermes_keys/` from `EXCLUDE_PATTERNS` so the private key never enters backup archives.

## Verified Result
- Backup ID: 20260530_135025
- 47.0 MB total, 10 items
- 3 encrypted secrets in `encrypted_secrets/` folder
- Git commit: aa57fd2