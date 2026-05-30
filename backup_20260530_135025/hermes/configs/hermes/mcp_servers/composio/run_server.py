#!/usr/bin/env python
import os
import asyncio
from composio.core.mcp.server import run_mcp_server # Correct import
from composio.core.mcp.server.config import Action, App, Config

# No direct client initialization needed here, run_mcp_server handles it
# based on COMPOSIO_API_KEY env var.

async def main():
    """
    Main function to create and run the MCP server.
    """
    print("Starting Composio MCP Server...")

    # Define the configuration for the MCP server.
    # This example includes a few common tools. You can add more.
    # A full list is available at https://docs.composio.dev/toolkits
    server_config = Config(
        apps=[
            App(
                name="github",
                actions=[
                    Action(id="create_issue"),
                    Action(id="get_issue"),
                    Action(id="list_issues"),
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
             App(
                name="trello",
                actions=[
                    Action(id="create_card"),
                    Action(id="get_cards"),
                ],
            )
        ]
    )

    print("Server configuration loaded.")

    # Start the server and listen for MCP requests
    print("Listening for MCP requests on stdio...")
    await run_mcp_server(config=server_config) # Call the correct function

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server stopped by user.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

