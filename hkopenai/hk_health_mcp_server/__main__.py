"""
Module serving as the entry point for the HK OpenAI Health MCP Server.
This script initiates the main server functionality.
"""



from hkopenai_common.cli_utils import cli_main
from .server import server

if __name__ == "__main__":
    cli_main(server, "HK Health MCP Server")