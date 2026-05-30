---
name: mcp-composio-hardening
description: "Production-grade reliability for Composio MCP: healthchecks, drift detection, auto-recovery, and compliance verification."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [composio, mcp, reliability, healthcheck, hardening]
---

# Composio MCP Hardening SOP

**Purpose:** Guarantee Composio MCP is reachable, authenticated, and tool-callable at all times. Detect drift before it causes failures.

## 1. Healthcheck Architecture

### Level 1: Config State (`hermes mcp list`)
- **What it checks:** Config registration only.
- **Limitation:** `✓ enabled` does NOT mean the server is reachable.
- **Command:** `hermes mcp list`

### Level 2: Connection Test (`hermes mcp test composio`)
- **What it checks:** TCP/TLS handshake + tool discovery.
- **Pass criteria:** `✓ Connected` + `✓ Tools discovered: 7`
- **Command:** `hermes mcp test composio`

### Level 3: Live Tool Call (Gold Standard)
- **What it checks:** End-to-end tool invocation from an agent session.
- **Why needed:** Level 1 and 2 can pass while Level 3 fails (cached schemas, stale OAuth).
- **Command:**
```bash
hermes chat -q "Use COMPOSIO_SEARCH_TOOLS to find GitHub tools. Return only 2-3 tool names." --quiet
```
- **Pass criteria:** Response contains real tool names (e.g., `GITHUB_GET_A_REPOSITORY`).

**Rule:** Always verify at Level 3 after ANY config change or MCP reload.

## 2. Automated Healthcheck Cron

Create a cron job that runs Level 2 + Level 3 checks on schedule:

```bash
# save as: ~/.hermes/scripts/composio_healthcheck.sh
#!/bin/bash
set -euo pipefail

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
REPORT="/home/hiryu/.hermes/vault/dev/composio_healthcheck_latest.txt"

# Level 2
echo "=== Composio Healthcheck $TIMESTAMP ===" > "$REPORT"
echo "" >> "$REPORT"
echo "[L2] Connection Test:" >> "$REPORT"
hermes mcp test composio >> "$REPORT" 2>&1 || true

# Level 3
echo "" >> "$REPORT"
echo "[L3] Live Tool Call:" >> "$REPORT"
RESULT=$(hermes chat -q "Call COMPOSIO_SEARCH_TOOLS to find Slack tools. Return just 2 tool names." --quiet 2>&1) || true
echo "$RESULT" >> "$REPORT"

# Verdict
if echo "$RESULT" | grep -qiE "SLACK_|slack"; then
    echo "" >> "$REPORT"
    echo "VERDICT: PASS" >> "$REPORT"
else
    echo "" >> "$REPORT"
    echo "VERDICT: FAIL" >> "$REPORT"
fi
```

Schedule via Hermes cron:
```
hermes cron create --schedule "0 */6 * * *" --prompt "Run Composio healthcheck" --name "Composio Healthcheck"
```

## 3. Drift Detection

### Config Drift
Check `config.yaml` composio block matches the canonical form:
```yaml
  composio:
    url: https://connect.composio.dev/mcp
    auth: oauth
    enabled: true
```

**Anti-patterns to detect and remove:**
- `mcp.servers.composio` duplicate block (legacy)
- `auth_config` with `client_id`/`client_secret` placeholders
- `allowed_tools` list (hosted endpoint manages this)
- `command`/`args`/`env` keys (local bridge — incorrect for hosted mode)

### Connection Drift
Compare tool count between healthchecks. If tool count drops below 7, investigate:
1. OAuth token expiry → `hermes mcp login composio`
2. Composio service outage → check status.composio.dev
3. Network/Firewall → `curl -sI https://connect.composio.dev/mcp`

## 4. Recovery Playbook

| Symptom | Diagnosis | Recovery |
|---------|-----------|----------|
| `✗ Connection failed` | TCP/TLS issue | Check network; `curl https://connect.composio.dev/mcp` |
| `✓ Connected` but 0 tools | OAuth token expired | `hermes mcp login composio` |
| `MCP server 'composio' is not connected` (in agent) | Stale session schemas | `/new` or restart Hermes |
| `not reachable after 7 failures` | Config corruption or `auth_config` keys | Strip config to canonical form; reload |
| `ModuleNotFoundError: composio.core.mcp` | Local bridge script running | Switch to hosted endpoint config |

## 5. Compliance Checklist

- [ ] Config matches canonical form (no extra keys)
- [ ] `hermes mcp list` shows composio enabled
- [ ] `hermes mcp test composio` passes with 7+ tools
- [ ] Live tool call succeeds (Level 3)
- [ ] No duplicate `mcp.servers.composio` block
- [ ] No local bridge `command`/`args` in composio block
- [ ] Healthcheck cron active and reporting
- [ ] Restore drill includes Composio config recovery
- [ ] Secret files (.env, auth.json, state.db) encrypted at-rest with age
- [ ] Encryption key stored in `hermes_keys/` (chmod 600, dir chmod 700)
- [ ] Encryption roundtrip verified (encrypt → decrypt → sha256sum match)
- [ ] Key excluded from backup archives (user carries key separately)

**References:**
- `references/secret-encryption-sop.md` — Full SOP for age-based secret encryption, key generation, roundtrip verification, and security invariants.