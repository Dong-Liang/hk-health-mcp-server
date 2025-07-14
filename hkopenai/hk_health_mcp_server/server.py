"""
Module for creating and running the HK OpenAI Health MCP Server.
This server provides tools for accessing health-related data in Hong Kong.
"""

from fastmcp import FastMCP
from hkopenai.hk_health_mcp_server import (
    tool_aed_waiting,
    tool_specialist_waiting_time_by_cluster,
    tool_pas_gopc_avg_quota,
)


def create_mcp_server():
    """
    Create and configure the MCP server for HK OpenAI Health services.
    This function initializes the server with necessary tools for health data access.

    Returns:
        FastMCP: Configured MCP server instance with health tools registered.
    """
    mcp = FastMCP(name="HK OpenAI Health Server")

    tool_aed_waiting.register(mcp)
    tool_specialist_waiting_time_by_cluster.register(mcp)
    tool_pas_gopc_avg_quota.register(mcp)

    return mcp



