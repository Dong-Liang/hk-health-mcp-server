"""
Module for creating and running the HK OpenAI Health MCP Server.
This server provides tools for accessing health-related data in Hong Kong.
"""

import argparse
from fastmcp import FastMCP
from hkopenai.hk_health_mcp_server import (
    tool_aed_waiting,
    tool_specialist_waiting_time_by_cluster,
    tool_pas_gopc_avg_quota,
)
from typing import Dict, Annotated, Optional
from pydantic import Field


def create_mcp_server():
    """
    Create and configure the MCP server for HK OpenAI Health services.
    This function initializes the server with necessary tools for health data access.
    
    Returns:
        FastMCP: Configured MCP server instance with health tools registered.
    """
    mcp = FastMCP(name="HK OpenAI Health Server")

    @mcp.tool(
        description="Get current Accident and Emergency Department waiting times by hospital in Hong Kong"
    )
    def get_aed_waiting_times(
        lang: Annotated[
            Optional[str],
            Field(
                description="Language (en/tc/sc) English, Traditional Chinese, Simplified Chinese. Default English",
                json_schema_extra={"enum": ["en", "tc", "sc"]},
            ),
        ] = "en",
    ) -> Dict:
        return tool_aed_waiting.get_aed_waiting_times(lang or "en")

    @mcp.tool(
        description="Get current waiting times for new case bookings for specialist outpatient services by specialty and cluster in Hong Kong"
    )
    def get_specialist_waiting_times(
        lang: Annotated[
            Optional[str],
            Field(
                description="Language (en/tc/sc) English, Traditional Chinese, Simplified Chinese. Default English",
                json_schema_extra={"enum": ["en", "tc", "sc"]},
            ),
        ] = "en",
    ) -> Dict:
        return tool_specialist_waiting_time_by_cluster.get_specialist_waiting_times(
            lang or "en"
        )

    @mcp.tool(
        description="Get average number of general outpatient clinic quotas for the preceding 4 weeks across 18 districts in Hong Kong"
    )
    def get_pas_gopc_avg_quota(
        lang: Annotated[
            Optional[str],
            Field(
                description="Language (en/tc/sc) English, Traditional Chinese, Simplified Chinese. Default English",
                json_schema_extra={"enum": ["en", "tc", "sc"]},
            ),
        ] = "en",
        district: Annotated[
            Optional[str],
            Field(
                description="Optional: Filter by district name (e.g., 'Tuen Mun'). If not provided, data for all districts will be returned."
            ),
        ] = "",
    ) -> Dict:
        return tool_pas_gopc_avg_quota.get_pas_gopc_avg_quota(
            lang or "en", district or ""
        )

    return mcp


def main():
    """
    Main function to run the MCP Server.
    Parses command line arguments to determine the mode of operation (SSE or stdio).
    """
    parser = argparse.ArgumentParser(description="MCP Server")
    parser.add_argument(
        "-s", "--sse", action="store_true", help="Run in SSE mode instead of stdio"
    )
    parser.add_argument(
        "--host", type=str, default="127.0.0.1", help="Host to bind the server to"
    )
    args = parser.parse_args()

    server = create_mcp_server()

    if args.sse:
        server.run(transport="streamable-http", host=args.host)
        print(f"MCP Server running in SSE mode on port 8000, bound to {args.host}")
    else:
        server.run()
        print("MCP Server running in stdio mode")


if __name__ == "__main__":
    main()
