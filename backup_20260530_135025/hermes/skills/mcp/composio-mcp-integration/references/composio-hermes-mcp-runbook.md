# Composio - Hermes Integration Runbook (v3 — June 2026)

## Status: Path A (Hosted) is the only working path

Path B (local bridge via `composio-core` SDK) is **broken** as of `composio-core >= 0.7.21`. The `composio.core.mcp` module no longer exists. Any bridge script using that import path will fail with `ModuleNotFoundError`.

## Path A — Hosted HTTP MCP (ACTIVE, WORKING)

### When to use
- Any situation where you want Composio tools via Hermes MCP.
- The only working path as of v3.

### Configuration (config.yaml)

```yaml
mcp_servers:
  composio:
    url: https://connect.composio.dev/mcp
    auth: oauth
    enabled: true
```

**DO NOT add:**
- `auth_config: {client_id: ..., client_secret: ...}` — this breaks OAuth flow
- `allowed_tools: [...]` — not a valid key for hosted MCP endpoints
- `command/args/env` — these are for local processes, not HTTP transports

### Step-by-step

```
# 1. Backup
cp ~/.hermes/config.yaml ~/.hermes/config.yaml.bak.$(date +%Y%m%d)

# 2. Set via hermes config (safe, non-interactive)
hermes config set mcp_servers.composio.url "https://connect.composio.dev/mcp"
hermes config set mcp_servers.composio.auth oauth
hermes config set mcp_servers.composio.enabled true

# 3. Reload MCP servers
# Hermes auto-reloads on config change. Use /reload-mcp in-session.

# 4. Verify
hermes mcp list
# Must show: composio ✓ enabled, Transport: HTTPS

# 5. Test connection
hermes mcp test composio
# Expected: ✓ Connected, ✓ Tools discovered: N
# Tools available: COMPOSIO_MANAGE_CONNECTIONS, COMPOSIO_MULTI_EXECUTE_TOOL,
# COMPOSIO_REMOTE_BASH_TOOL, COMPOSIO_REMOTE_WORKBENCH,
# COMPOSIO_SEARCH_TOOLS, COMPOSIO_WAIT_FOR_CONNECTIONS, COMPOSIO_GET_TOOL_SCHEMAS

# 6. Auth (if token expired)
hermes mcp login composio
# Completes OAuth in a separate terminal
```

### Verification checklist

- [ ] `hermes mcp list` shows composio ✓ enabled, HTTPS transport
- [ ] `hermes mcp test composio` shows ✓ Connected + tool count
- [ ] Live tool call succeeds (e.g., `COMPOSIO_SEARCH_TOOLS`)
- [ ] Native servers (filesystem, github, time) still listed
- [ ] Backup exists before any config mutation

## Path B — Local Bridge (DEPRECATED, DO NOT USE)

### Why it broke
In `composio-core >= 0.7.21`, the `composio.core.mcp` module was removed.
Scripts using:
```python
from composio.core.mcp.server import run_mcp_server
```
will fail with:
```
ModuleNotFoundError: No module named 'composio.core.mcp'
```

Even though `composio-core[mcp]` pip install succeeds, the module is gone.

### Old runbook (reference only, DO NOT USE)
```
command: /home/hiryu/.hermes/mcp_servers/composio/venv/bin/python
args:
  - /home/hiryu/.hermes/mcp_servers/composio/run_server.py
env:
  COMPOSIO_API_KEY: ${COMPOSIO_API_KEY}
```
This was the intended setup but will not work.

## Common failures

| Symptom | Cause | Fix |
|---|---|---|
| `hermes mcp test` shows HTTPS ✓ but live call fails | Token expired | `hermes mcp login composio` |
| Tool call returns "not connected" in-session | Session loaded old schemas | Start fresh session (`/new`) |
| Adding `auth_config` breaks OAuth | Key not valid for hosted mode | Remove `auth_config` entirely |
| Adding `allowed_tools` breaks connection | Not supported for hosted MCP | Remove entirely |
