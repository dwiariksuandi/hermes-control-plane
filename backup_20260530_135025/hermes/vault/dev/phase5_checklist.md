# Phase 5.1: Baseline & Guardrail Checklist

## ✅ Mandatory Verification Steps (All Must Pass)

### ✅ 1. Configuration Lockdown
- [ ] `config.yaml` contains **exactly** this `composio` block:
  ```yaml
  composio:
    url: https://connect.composio.dev/mcp
    auth: oauth
    enabled: true
  ```
- [ ] No duplicate `mcp.servers.composio` block exists
- [ ] No `auth_config`, `allowed_tools`, `command`, `args`, or `env` keys in `composio` block

### ✅ 2. Cron Integrity
- [ ] Total cron jobs = 5 (verified via `cronjob list`)
- [ ] No overlapping schedules (use `cronjob list` output)
- [ ] Jitter applied to avoid sync storms (e.g., `30 3 * * *` not `0 3 * * *` for all)

### ✅ 3. Backup Verification
- [ ] Backup size verified: `ls -lh /home/hiryu/.hermes/vault` shows ~2.1G
- [ ] `manifest_20260530_115107.json` exists and is valid JSON
- [ ] `retention_20260530_121212.json` exists and shows dry-run results
- [ ] `.env` and `.env.bak` files are present and redacted (`[REDACTED]`)

### ✅ 4. Tool & MCP Readiness
- [ ] `hermes mcp test composio` → `✓ Connected` + `✓ Tools discovered: 7`
- [ ] `hermes mcp list` → `composio` shows `✓ enabled`
- [ ] `hermes chat -q "Use COMPOSIO_SEARCH_TOOLS to find GitHub tools"` → returns real tool names (e.g., `GITHUB_GET_A_REPOSITORY`)

### ✅ 5. Evidence Ledger
- [ ] `/home/hiryu/.hermes/vault/dev/CLEAN_SLATE_LEDGER.md` exists (2.2K, 47 lines)
- [ ] Ledger contains entries for:
  - Backup cleanup (12G → 2.1G)
  - Cron cleanup (8 jobs → 5 jobs)
  - Retention engine v3 deployment
  - Compoio integration verification

## 🚫 Non-Negotiable Rules
- **NO** destructive changes without `approval` (verified by `todo` item status)
- **NO** cron job without `notify_on_complete=true`
- **NO** secret in logs (all secrets must be `[REDACTED]`)

## 📝 How to Verify
1. Run all commands listed above
2. Capture output in a log file (`/tmp/phase5_verify.log`)
3. Cross-check with `phase5_checklist.md` and `CLEAN_SLATE_LEDGER.md`
4. If any step fails → **STOP** and document root cause before proceeding

**Next Step**: After verifying all ✅ items, proceed to Phase 5.2 (Restore Drill).