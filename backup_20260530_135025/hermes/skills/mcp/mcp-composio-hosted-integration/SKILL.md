---
name: mcp-composio-hosted-integration
description: "SOP for integrating Composio MCP via Hosted Endpoint (Path A) robustly."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [composio, mcp, integration, oauth, hosted]
---

# Composio MCP Hosted Integration SOP

**Core Rule:** Always use the Hosted Endpoint (Path A) for Composio integration. Do NOT attempt to build a local bridge script (`composio-core` missing local MCP modules). Do NOT add custom `auth_config` or `allowed_tools` keys under the hosted configuration, as this breaks the connection.

## 1. Setup Configuration
Edit `~/.hermes/config.yaml` and ensure the `composio` block under `mcp_servers` strictly follows this format:

```yaml
mcp_servers:
  composio:
    url: https://connect.composio.dev/mcp
    auth: oauth
    enabled: true
```
*Note: Remove any legacy `mcp.servers.composio` duplicate block. Remove `command`, `args`, `auth_config`, and `allowed_tools` if present.*

## 2. Authentication
Run the OAuth login flow in a clean terminal:
```bash
hermes mcp login composio
```
Follow the browser prompts to authorize your tools (e.g., GitHub, Google Drive).

## 3. Verification & Live Test
Verify the connection using three layers of checks:

**A. Config State Check**
```bash
hermes mcp list
# Must show: composio  https://connect.composio.dev/mcp  all  ✓ enabled
```

**B. Connection Test**
```bash
hermes mcp test composio
# Must show: ✓ Connected and list discovered tools (e.g., COMPOSIO_SEARCH_TOOLS)
```

**C. Live Agent Test (Crucial)**
A live test in a fresh session ensures schemas are loaded properly.
```bash
hermes chat -q "Use COMPOSIO_SEARCH_TOOLS to find GitHub tools. Return just 2-3 tool names." --quiet
```
*If this fails with "not connected", schemas might be cached or the session is stale. Ensure you use a new session (`/new` or fresh CLI run).*

## 4. Troubleshooting Pitfalls
- **"ModuleNotFoundError: No module named 'composio.core.mcp'"**: You are trying to run the legacy local bridge script. Abort and switch to the hosted config above.
- **"MCP server 'composio' is unreachable after 7 consecutive failures"**: Usually caused by invalid keys in `config.yaml` like `auth_config: ... [REDACTED]`. The hosted endpoint handles auth externally. Strip the config down to just `url`, `auth: oauth`, and `enabled: true`.
- **"MCP server 'composio' is not connected" (in chat)**: The running Hermes process hasn't loaded the new MCP schemas. Restart the process or use `/reset`.