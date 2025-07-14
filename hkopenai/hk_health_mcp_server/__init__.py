"""Hong Kong Health MCP Server package."""

from hkopenai_common.cli_utils import cli_main
from .server import create_mcp_server

if __name__ == "__main__":
    cli_main(create_mcp_server, "HK Health MCP Server")
