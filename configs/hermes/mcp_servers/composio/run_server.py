#!/usr/bin/env python
"""
Hermes-Composio MCP Launcher
Starts a composio.com MCP server (stdio transport).
Uses COMPOSIO_API_KEY environment variable for authentication.
"""
import os
import asyncio
from composio.core.mcp.server import run_mcp_server
from composio.core.mcp.server.config import Action, App, Config

async def main() -> None:
    print("🔧 Starting Hermes Compose-MCP server …")

    # ----------------------  SERVER CONFIGURATION  ----------------------
    # Add/remove toolkits here – they will automatically appear as
    # mcp_<toolkits>_XXXX tools once the server boots.
    server_cfg = Config(
        apps=[
            App(
                name="github",
                actions=[
                    Action(id="create_issue"),
                    Action(id="list_issues"),
                ],
            ),
            App(
                name="gmail",
                actions=[
                    Action(id="list_messages"),
                ],
            ),
            App(
                name="linear",
                actions=[
                    Action(id="create_issue"),
                ],
            ),
            App(
                name="slack",
                actions=[
                    Action(id="send_message"),
                ],
            ),
            # Add any additional toolkits you need …
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