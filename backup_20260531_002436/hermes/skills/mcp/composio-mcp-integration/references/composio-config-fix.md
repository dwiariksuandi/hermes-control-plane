# Composio MCP Config Fix - May 2026

## Problem
Adding `allowed_tools` and `auth_config` blocks to `mcp_servers.composio` in `config.yaml` caused the MCP server to disconnect on reload. Hermes emitted:
```
MCP Servers:
  composio    https://connect.composio.dev/mcp    all    ✗ disabled
```

## Root Cause
- `allowed_tools` and `auth_config` are NOT valid keys for Composio-hosted HTTP MCP endpoints.
- These keys are for local bridge setups (Path B in runbook) or SDK server creation.
- Hermes' MCP loader treats unknown keys as malformed config → server marked disabled.

## Fix
1. Remove `allowed_tools` and `auth_config` from `config.yaml`.
2. Keep only:
```yaml
mcp_servers:
  composio:
    url: https://connect.composio.dev/mcp
    auth: oauth
    enabled: true
```
3. Run `hermes mcp reload` or restart Hermes session.
4. Complete OAuth flow: `hermes mcp login composio` in fresh terminal.

## Evidence
- Session: 2026-05-30T08:22
- Config diff: lines 552-563 showed invalid keys.
- After removal: `hermes mcp list` restored Composio with `✓ enabled`.