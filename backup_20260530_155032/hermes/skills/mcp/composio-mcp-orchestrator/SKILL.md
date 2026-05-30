---
name: composio-mcp-orchestrator
description: "Advanced orchestration and health monitoring for Composio MCP integration with Hermes Agent"
version: 1.0.0
author: Hermes Orchestrator
tags: ["composio", "mcp", "monitoring", "automation", "github", "integrations"]
---

# Composio MCP Orchestrator

**Purpose:** Comprehensive monitoring, health checking, and operation management for Composio MCP integration in Hermes Agent.

## Features

- 🔍 **Real-time health checks**
- 📊 **Connection status tracking**  
- 🔧 **Tool discovery validation**
- 🚨 **Automated issue detection**
- 🔄 **Recovery automation**
- 📈 **Performance metrics**

## Usage

```bash
# Manual health check
/composio-check

# Force connection refresh
/composio-refresh

# View connection details
/composio-status

# Test specific tool
/composio-test-tool GITHUB_GET_THE_AUTHENTICATED_USER
```

## Health Check Workflow

1. **Connection Validation** - Checks GitHub, Linear, and other app connections
2. **Tool Discovery** - Validates MCP tool availability and schemas
3. **Performance Benchmark** - Measures API response times
4. **Error Detection** - Scans for common failure patterns
5. **Recovery** - Attempts automatic reconnection when possible

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| GitHub connection failed | Re-run `hermes mcp test composio` and check GitHub token |
| Tool not found | Use `/composio-test-tool` to validate specific tools |
| MCP server down | Restart with `hermes mcp test composio --force` |
| Auth expired | Re-auth via `hermes auth add github` |

## Integration Notes

- **MCP Server:** `/home/hiryu/.hermes/mcp_servers/composio/run_server.py`
- **Config:** `/home/hiryu/.hermes/config.yaml`
- **Cron:** Health check runs every 6h (job ID: `b539fe95f9c1`)
- **Backup Reports:** `/home/hiryu/.hermes/vault/dev/`

## Security

- All tokens stored in `/home/hiryu/.hermes/.env` 
- Health logs scrub sensitive data automatically
- No credentials exposed in telemetry