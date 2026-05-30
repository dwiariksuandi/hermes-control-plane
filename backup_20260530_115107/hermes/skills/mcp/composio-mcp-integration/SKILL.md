---
name: composio-mcp-integration
description: Integrate Composio with Hermes Agent via MCP without breaking native tools.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [composio, mcp, hermes, integration, oauth, tool-isolation]
---

# Composio MCP Integration (Hermes)

## When to use
- User wants Composio added to Hermes.
- Requirement: keep native Hermes tools active and non-overlapping.
- Requirement: clean credential handling and rollback path.

## Core outcome
- Composio exposed through MCP namespace (`mcp_composio_*`).
- Native tools (`terminal`, `file`, `browser`, `delegate_task`, etc.) unchanged.
- Config backup created before mutation.

## Procedure (v3 - May 2026)
Composio can be integrated two ways. Choose path based on endpoint type.

### Path A — Hosted HTTP MCP endpoint (preferred when user provides URL)
Use this when user gives `https://.../mcp` endpoint and wants OAuth.

1. **Backup config first** (`~/.hermes/config.yaml.bak`).
2. **Set URL directly**:
   - `hermes config set mcp_servers.composio.url "https://connect.composio.dev/mcp"`
3. **Set OAuth mode explicitly**:
   - `hermes config set mcp_servers.composio.auth oauth`
4. **Verify registration**:
   - `hermes mcp list` (must show `composio` enabled with HTTPS transport)
5. **Complete auth in fresh terminal**:
   - `hermes mcp login composio`

### Path B — Legacy/local bridge path
Use only when user specifically needs local bridge workflow.

1. **Create isolated venv** for the Composio SDK.
2. **Install the correct package**: `pip install composio-core`. The `composio-sdk` package is obsolete.
3. **Obtain API Key** from the user and store it securely (e.g., in `~/.hermes/.env`).
4. **Architectural Mismatch**: Recognize that Composio provides a remote URL (`session.mcp.url`) while Hermes's `config.yaml` expects a local `command` to execute.
5. **Bridge Implementation**: Write local Python script (`run_server.py`) that:
   a. Initializes Composio client using API key.
   b. Fetches dynamic tool schemas from Composio API.
   c. Uses `mcp` library (`pip install mcp`) to expose fetched schemas locally.
6. **Configure Hermes**: Point `~/.hermes/config.yaml` to local bridge script.
7. **Verify**: `hermes mcp list` and `hermes mcp test composio`.

## Verification checklist (must show evidence)
- `hermes mcp list` shows `composio` enabled.
- `hermes mcp test composio` passes.
- At least one Composio tool callable in a **fresh Hermes session** (do not rely on current long-lived session if MCP config/auth changed mid-session).
- Native servers (`time`, `filesystem`, `github`) still listed.
- Backup file exists for config mutation.

### Evidence reporting rule (anti-empty-response)
After running verification commands, always return a human summary immediately in same turn. Do not stop after tool execution output only. Include: transport mode, auth mode, test result, discovered tool count, and next action if any.

### Runtime truth check (important)
- `enabled` in `hermes mcp list` only means config registration, not live connectivity.
- If `hermes mcp test composio` passes but an existing chat session's native `mcp_composio_*` tool call returns `MCP server 'composio' is not connected`, the active agent session likely loaded MCP schemas before the config/auth change. Do not diagnose this as a Composio outage first.
- Recovery order:
  1. `hermes mcp login composio`
  2. `hermes mcp test composio`
  3. start a fresh Hermes session (`/new`, restart `hermes`, or `hermes chat -q ...`) so MCP schemas reload
  4. re-run a minimal tool call (`COMPOSIO_SEARCH_TOOLS` or equivalent)
- For final proof after mid-session MCP changes, use a fresh one-shot session, e.g. `hermes chat -q "Use COMPOSIO_SEARCH_TOOLS to find available GitHub tools in Composio. Return concise list." --quiet`.

## Pitfalls
- **`hermes mcp add` interactive flow**: The interactive prompt for `hermes mcp add` is not suitable for OAuth-based HTTP servers. It times out after 30 seconds, which is not enough time to complete a browser-based OAuth flow. **Always configure OAuth servers by directly editing `config.yaml`** (e.g., via `hermes config set ...`) and then use `hermes mcp login <name>` to initiate the auth flow from a fresh terminal.
- **Architectural Mismatch**: Do not try to find a local server command in the modern Composio SDK. It provides a remote endpoint that must be bridged for Hermes.
- **Incorrect Package**: Do not `pip install composio-sdk`; the correct package is `composio-core`.
- **Broken CLI**: The `composio` CLI tool included with `composio-core==0.7.21` may be broken due to a `click` dependency issue (`TypeError: EnumParam.get_metavar() got an unexpected keyword argument 'ctx'`). Do not rely on it for setup.
- **Do not replace native toolsets** with Composio; run side-by-side.
- **Do not store API key in ad-hoc scripts** longer than needed. Use env-based injection.
- **Package name changes:** As of v0.7.21, `composio-sdk` and `composio-mcp` are no longer valid on PyPI. `composio-core` installs but its MCP server import paths (`composio.core.mcp` or `composio.mcp`) may have changed. Always verify the correct package and import paths from current Composio documentation before writing the launcher script.

## Security
- Redact keys in chat/logs.
- Prefer env-based secret injection in `mcp_servers.<name>.env`.
- Delete temp files containing secrets after successful integration.

## References
- `references/composio-hermes-mcp-runbook.md` — proven flow, sample config, and cleanup steps.
