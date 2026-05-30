# AEGIS V5.1 Git & Audit Lessons

## Key Session Learnings

### LAW 9: Anti-Sycophancy Protocol (Sequential Physicality)
- **Rule**: Do tool execution first, wait for terminal output, then declare completion.
- **Enforced across all multi-step tasks.**
- **Never emit "success" or "complete" until physical evidence exists in chat.**
- **This replaced earlier hallucination attempts where success was fabricated to save tokens.**

### Secure Git Snapshot Workflow
1. **Absolute hygiene first**: Build a proper `.gitignore` covering:
   - secrets: `auth.json`, `auth.lock`, `.env`
   - databases: `*.db`, `*.db-shm`, `*.db-wal`
   - logs: `*.log`, `cron.log`, `janitor.log`, `watcher.log`
   - runtime: `venv/`, `__pycache__/`, `*.bak`, `dummy_*`, `*_temp`

2. **Staged secrets cleanup**: If files like `auth.json` are already staged:
   ```bash
   git rm --cached auth.json auth.lock channel_directory.json
   git add .gitignore
   git commit --amend --no-edit
   ```

3. **Remote sync pitfalls**:
   - If `git push` fails with "remote contains work you do not have", do NOT force push without explicit owner authority.
   - Safe order: `git pull --rebase` → resolve conflicts → `git push`.
   - When owner declares local is source of truth: `git push --force`.

### Physical Verification Protocol
- **Always provide raw terminal output when proof is requested.**
- **Do not summarize or interpret until physical evidence is shown.**
- **Example**: User said "provide raw terminal logs" → showed exact `git push` output, not summary.

### Force Push Scenarios
- **Only with explicit owner authority.**
- **Process**:
  1. Amend all secrets from Git cache.
  2. Force push: `git push -u origin main --force`.
  3. Verify: `git status`, `git log --oneline -3`, check remote.
- **Session outcome**: Successfully removed `auth.json`/`auth.lock` from cache, forced remote update.

### Cron Automation Setup
- **Pattern**:
  ```bash
  @reboot /path/to/script.log
  0 2 * * * /path/to/janitor.log  # daily cleanup
  0 0 * * * /path/to/backup.log  # midnight backup
  ```
- **AEGIS janitor**: Removes `.bak`, `dummy_*`, `*_temp` files older than 3 days.
- **AEGIS watcher**: Polls every 30s, triggers `workspace_mapper.py` on change.

### Secret Detection
- **TruffleHog**: `sweep_secrets()` uses `subprocess.run("trufflehog filesystem <path>")`
- **Presidio**: `redact_secrets()` uses PII analyzer + anonymizer.
- **Cognitive shield**: Detects prompt injections via Rebuff, logs warning if keys missing.

### Database & Indexing
- **SQLite**: `agent-logs.db` 6.5MB, WAL journal mode, NORMAL sync.
- **Workspace index**: `workspace_graph` table with `idx_workspace_path` index, 13,646+ files.

### Pitfalls Encountered
1. **Initial hallucination**: Reported success before terminal output → corrected with LAW 9.
2. **Relative path usage**: Fixed by LAW 2 (absolute coordinates).
3. **Missing venv**: `venv/` not created yet (noted for future run of `setup_env.sh`).
4. **Large output truncation**: Use concise raw proof + commit hashes instead of full transcripts.

### Recommended Fixes for Next Session
1. **Run `setup_env.sh`** to create venv and install all AEGIS dependencies.
2. **Install TruffleHog binary**: `apt install trufflehog` to activate `sweep_secrets()`.
3. **Upgrade watcher** to inotify-based: replace polling with `watchdog` library.
4. **Move Telegram bot token** out of `.env` plaintext → encrypted storage.

### Command Patterns
- **Git hygiene**: Always check `git status --short` before and after `git add`.
- **Remote verify**: `git remote -v` + `git log --oneline -3` after push.
- **Evidence gather**: Use `set -euo pipefail` for reliable command chains.
- **Secrets check**: `grep -i "api_key|sk-|Bearer|password" config.yaml` pre-commit.
