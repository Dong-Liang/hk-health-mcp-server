"""
Module for testing the MCP server creation and tool functionality.
This module contains unit tests to verify the behavior of the server setup.
"""

import unittest
from unittest.mock import patch, Mock
from hkopenai.hk_health_mcp_server.server import create_mcp_server


class TestApp(unittest.TestCase):
    """
    Test class for verifying MCP server functionality.
    This class contains tests to ensure the server and its tools are set up correctly.
    """

    @patch("hkopenai.hk_health_mcp_server.server.FastMCP")
    @patch("hkopenai.hk_health_mcp_server.server.tool_aed_waiting")
    @patch(
        "hkopenai.hk_health_mcp_server.server.tool_specialist_waiting_time_by_cluster"
    )
    @patch("hkopenai.hk_health_mcp_server.server.tool_pas_gopc_avg_quota")
    def test_create_mcp_server(
        self,
        mock_tool_pas_gopc_avg_quota,
        mock_tool_specialist_waiting_time_by_cluster,
        mock_tool_aed_waiting,
        mock_fastmcp,
    ):
        """
        Test the creation of the MCP server and its tool integrations.
        Verifies that the server is initialized correctly and tools are properly decorated.
        """
        # Setup mocks
        mock_server = Mock()

        # Configure mock_server.tool to return a mock that acts as the decorator
        # This mock will then be called with the function to be decorated
        mock_server.tool.return_value = Mock()
        mock_fastmcp.return_value = mock_server

        # Test server creation
        server = create_mcp_server()

        # Verify server creation
        mock_fastmcp.assert_called_once()
        self.assertEqual(server, mock_server)

        mock_tool_aed_waiting.register.assert_called_once_with(mock_server)
        mock_tool_specialist_waiting_time_by_cluster.register.assert_called_once_with(
            mock_server
        )
        mock_tool_pas_gopc_avg_quota.register.assert_called_once_with(mock_server)


if __name__ == "__main__":
    unittest.main()
