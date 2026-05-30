---
name: composio-integration
description: "Integrate Composio with Hermes Agent for unified SaaS API access via MCP"
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
tags: [composio, mcp, saas, integration, api]
---

# Composio Integration with Hermes Agent

This skill provides a clean, isolated pattern for integrating Composio (SaaS integration platform) with Hermes Agent using the built-in MCP client. It maintains separation between Composio tools and native Hermes tools to prevent overlap.

## When to Use This Skill

Use this skill when you need to:
- Access 1000+ SaaS applications (GitHub, Slack, Notion, Linear, etc.) through a unified interface
- Avoid writing custom API wrappers for each service
- Maintain secure, managed authentication for multiple services
- Integrate with Hermes without disrupting native tool functionality
- Create scalable, reusable integrations for production workflows

## Key Benefits

- **Unified Access**: Single interface for 1000+ SaaS tools via Composio's MCP server
- **Managed Auth**: OAuth/API key handling automated by Composio
- **Isolation**: Composio tools namespaced as `mcp_composio_*`, separate from native tools
- **Fallback Safety**: Native Hermes tools remain fully functional if Composio integration fails
- **Security**: Follows SOUL.md principles for secret redaction and verification

## Prerequisites

1. **Composio Account**: Sign up at [composio.dev](https://composio.dev) and obtain an API key
2. **Python Environment**: Isolated virtual environment for Composio dependencies
3. **Hermes MCP Client**: Built-in MCP support (requires `mcp` Python package)

## Installation & Setup

### 1. Create Isolated Environment for Composio

```bash
# Create dedicated directory and virtual environment
mkdir -p ~/.hermes/mcp_servers/composio
uv venv ~/.hermes/mcp_servers/composio/venv

# Install Composio SDK in the isolated environment
~/.hermes/mcp_servers/composio/venv/bin/pip install composio
```

### 2. Create MCP Server Launcher Script

Save this as `~/.hermes/mcp_servers/composio/run_server.py`:

```python
#!/usr/bin/env python
"""
Hermes-Composio MCP Launcher
Starts a Composio MCP server (stdio transport).
Uses COMPOSIO_API_KEY environment variable for authentication.
"""
import asyncio
from composio.core.mcp.server import run_mcp_server
from composio.core.mcp.server.config import Action, App, Config

async def main() -> None:
    """Start the Composio MCP server."""
    print("🔧 Starting Hermes Compose-MCP server …")

    # Define toolkits - they become mcp_<toolkit>_<action> tools
    server_cfg = Config(
        apps=[
            App(
                name="github",
                actions=[
                    Action(id="create_issue"),
                    Action(id="list_issues"),
                    Action(id="get_issue"),
                    Action(id="create_pull_request"),
                    Action(id="merge_pull_request"),
                ],
            ),
            App(
                name="linear",
                actions=[
                    Action(id="create_issue"),
                    Action(id="list_issues"),
                ],
            ),
            App(
                name="slack",
                actions=[
                    Action(id="send_message"),
                    Action(id="get_channels"),
                ],
            ),
            # Add more toolkits as needed
        ]
    )

    print("✅ Config loaded – listening for MCP requests on stdio …")
    await run_mcp_server(config=server_cfg)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("🛑 Server stopped by user.")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
```

### 3. Configure Hermes Agent

Edit `~/.hermes/config.yaml` and add under the `mcp_servers` section:

```yaml
mcp_servers:
  # ... other servers ...
  composio:
    command: "/home/hiryu/.hermes/mcp_servers/composio/venv/bin/python"
    args: ["/home/hiryu/.hermes/mcp_servers/composio/run_server.py"]
    env:
      COMPOSIO_API_KEY: "your_actual_api_key_here"  # Get from composio.dev
    timeout: 120
    connect_timeout: 30
```

### 4. Restart Hermes Agent

A full restart is required for Hermes to detect the new MCP configuration:
```bash
hermes  # or however you normally start it
```

## Usage in Hermes Agent

After successful setup, Composio tools will be available with the prefix `mcp_composio_*`.

### Examples

```bash
# List available Composio tools
hermes chat -q "List tools that start with mcp_composio_"

# Create a GitHub issue
hermes chat -q "Use mcp_composio_github_create_issue with title 'Test issue' and body 'This is a test'"

# Send a Slack message
hermes chat -q "Use mcp_composio_slack_send_message with channel '#general' and text 'Hello from Hermes!'"

# Add a record to Airtable
hermes chat -q "Use mcp_composio_airtable_create_record with base_id='appXXXXXX', table_id='tblXXXXXX', and fields={'Name': 'Test Record'}"
```

## Verification (VBC - Verification Before Completion)

After each integration step, verify using these checks:

1. **Environment Setup**: Confirm venv and package installation
   ```bash
   ~/.hermes/mcp_servers/composio/venv/bin/python -c "import composio; print('Composio version:', composio.__version__)"
   ```

2. **Server Launch**: Test the launcher script manually
   ```bash
   timeout 10 ~/.hermes/mcp_servers/composio/venv/bin/python ~/.hermes/mcp_servers/composio/run_server.py
   ```
   (Should start and wait for MCP connections)

3. **Hermes Detection**: Check Hermes startup logs for MCP server connection
   - Look for: "Connected to MCP server: composio"
   - Verify tools appear: `mcp_composio_github_create_issue`, etc.

4. **Tool Execution**: Execute a simple, non-destructive command and verify output
   ```bash
   hermes chat -q "Use mcp_composio_github_get_user to get your GitHub profile"
   ```
   Check that you receive valid JSON response with user data.

## Security & Best Practices

### Secret Management (SOUL.md Compliance)
- **Never** expose `COMPOSIO_API_KEY` in chat, logs, or scripts
- Store API key only in `.env` or Hermes config (which is already protected)
- Hermes automatically filters environment variables for MCP subprocesses
- Enable secret redaction: `hermes config set security.redact_secrets true`

### Tool Isolation
- Composio tools appear as `mcp_composio_*` - never conflict with native tools
- Native tools (`terminal`, `read_file`, `git`, etc.) remain fully accessible
- Use `delegate_task` to isolate Composio work to specific sub-agent profiles if needed

### Error Handling & Fallbacks
- Implement retry logic (max 3 attempts) for transient failures
- Have fallback plans using native tools (e.g., `terminal` + `curl` for simple API calls)
- Monitor connection health via Hermes telemetry/logs

## Troubleshooting

### Clean Reinstall (Nuke & Pave)

When `composio upgrade` fails or the CLI is in a corrupted state, a clean reinstall is the most reliable fix.

1.  **Backup Critical Config**: The only file worth preserving is `user_data.json` which contains the API key and organization details.
    ```bash
    cp ~/.composio/user_data.json ~/.composio_user_data.bak
    ```
2.  **Remove Old Installation** (Destructive)
    ```bash
    rm -rf ~/.composio
    ```
3.  **Fetch Latest Release & Install**: Download the latest binary directly from the official source.
    ```bash
    curl -L -o ~/.composio/composio "https://github.com/ComposioHQ/composio-cli/releases/latest/download/composio-$(uname -s | tr '[:upper:]' '[:lower:]')-$(uname -m | sed 's/x86_64/amd64/')"; chmod +x ~/.composio/composio
    ```
4.  **Restore Config**: Move the critical config back into place.
    ```bash
    mkdir -p ~/.composio
    mv ~/.composio_user_data.bak ~/.composio/user_data.json
    ```
5.  **Verify PATH**: Ensure `~/.composio` is in your shell's PATH. Add it to `~/.bashrc` or `~/.profile` if missing.
    ```bash
    echo 'export PATH="$HOME/.composio:$PATH"' >> ~/.bashrc
    source ~/.bashrc
    ```
6.  **Final Verification**: Check that the new version is installed and authenticated.
    ```bash
    composio --version
    composio whoami
    ```

### Common Issues & Fixes

**"API Key not provided" Error**
- Ensure `COMPOSIO_API_KEY` is set in the env section of config.yaml
- Verify the key is valid at composio.dev
- Check for typos or extra spaces

**"ModuleNotFoundError: No module named 'composio'"**
- Confirm the venv path is correct in config.yaml
- Reinstall: `~/.hermes/mcp_servers/composio/venv/bin/pip install composio`

**Server fails to start**
- Test launcher script manually first
- Check composio service status at status.composio.dev
- Verify network connectivity to composio servers

**Tools not appearing in Hermes**
- Restart Hermes after config changes
- Check Hermes logs for MCP connection messages
- Verify tool naming: `mcp_composio_<toolkit>_<action>`

**Connection drops frequently**
- Increase `connect_timeout` in config (try 60s)
- Check for network interference or firewall issues
- The client automatically retries with exponential backoff

## Advanced Patterns

### Multi-Profile Isolation
Create dedicated profiles for different integration needs:
```bash
hermes profile create composio-worker --clone-from default
# Then configure only that profile with Composio MCP settings
```

### Event-Driven Workflows
Use Composio Triggers with Hermes:
1. Set up trigger in Composio dashboard (e.g., "GitHub issue created")
2. Configure webhook to call Hermes MCP endpoint
3. Hermes processes event via standard tool calling

### Rate Limiting & Quotas
- Composio enforces rate limits per toolkit
- Monitor usage in composio.dev dashboard
- Implement retry-with-backoff in orchestration logic

## Related Skills

- `native-mcp`: Core MCP client functionality in Hermes
- `kanban-orchestrator`: For managing complex integration workflows
- `webhook-subscriptions`: For event-driven integration patterns
- `vm-pip-bootstrap`: For managing isolated Python environments

## Maintenance
## User-Specific Workflow Preferences

### Clean Reinstall Policy
When performing a clean reinstall of the Composio CLI for this user, **do not backup** the existing `~/.composio` directory unless explicitly requested. The user prefers a "very clean and tidy" (sangat bersih dan rapi) state and often provides their own backup strategy or deems the old state unnecessary.

- Default action for reinstall: `rm -rf ~/.composio` followed by fresh install.
- Verification: Always verify new version and API connectivity post-install.

## Maintenance
### Backup & Restore Reference
See `references/backup-restore.md` for a complete one-click backup/restore pattern using SSH push to GitHub and secret-safe Composio MCP restoration.

### Updating Composio SDK
```bash
~/.hermes/mcp_servers/composio/venv/bin/pip install --upgrade composio
```

### Composio CLI installer/version mismatch
If `curl -fsSL https://composio.dev/install | bash` reports a newer tag but `~/.composio/composio --version` stays older, use the manual asset workflow in `references/manual-cli-install.md`.

Short rule:
- Do not trust only `releases/latest` (monorepo latest may not be CLI)
- Enumerate `@composio/cli@*` releases with assets
- Download exact `composio-linux-x64.zip` and replace binary manually

### Adding New Toolkits
1. Edit `run_server.py` to add new `App` entries
2. Restart Hermes Agent to pick up changes
- Verify new tools appear with correct naming

### Removing Integration
1. Remove `composio` section from `mcp_servers` in config.yaml
2. Restart Hermes Agent
3. Optionally remove the `~/.hermes/mcp_servers/composio/` directory

---
## References
- Composio Documentation: https://docs.composio.dev
- MCP Specification: https://modelcontextprotocol.io
- Composio MCP Guide: https://docs.composio.dev/docs/mcp
- SOUL.md Absolute Laws: Refer to Hermes Agent's core governance
- venv-pip-bootstrap skill: For virtual environment management