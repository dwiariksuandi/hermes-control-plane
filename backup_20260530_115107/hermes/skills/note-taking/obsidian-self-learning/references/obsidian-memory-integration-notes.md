# Obsidian Memory Integration Notes

## Critical Distinctions

1. **Hermes Memory Backend vs. Obsidian Vault**
   - Hermes has a built-in memory system (memory tools, MEMORY.md, USER.md).
   - Obsidian vault is a *filesystem layer* of Markdown notes.
   - They are NOT the same. Syncing is a bridge, not native integration.

2. **OBSIDIAN_VAULT_PATH Pitfall**
   - The env var is NOT automatically visible inside already-running tool sandboxes.
   - Must read `.env` directly or restart the gateway.
   - Always use absolute path `/home/hiryu/.hermes/vault` in scripts/sub-agents.

3. **Sync Policy**
   - Default: Runtime (Hermes) -> Vault (mirror).
   - Pull mode: Vault -> Runtime (only when human explicitly edits vault).
   - Conflict: log to `/home/hiryu/.hermes/vault/logs/memory-conflicts-YYYY-MM.md`.

## Automation Scripts

- `scripts/sync_memory_vault.py` - Two-way sync
- `scripts/capture_learning.py` - Append structured learning
- `scripts/dashboard_refresh.py` - Update dashboard
- `scripts/weekly_digest.py` - Generate weekly digest
- `scripts/backup_vault_git.sh` - Backup vault to private GitHub

## Cron Jobs

1. Hourly: `sync_memory_vault.py`
2. Daily 03:00: `dashboard_refresh.py`
3. Weekly Sunday 04:00: `weekly_digest.py`

## Verification Checklist

After any write:
- File exists
- File size > 0
- Last modified timestamp changed
- Output summary file path present