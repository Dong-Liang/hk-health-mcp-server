import unittest
from unittest.mock import patch, Mock
from hkopenai.hk_health_mcp_server.server import create_mcp_server

class TestApp(unittest.TestCase):
    @patch('hkopenai.hk_health_mcp_server.server.FastMCP')
    @patch('hkopenai.hk_health_mcp_server.server.tool_aed_waiting')
    @patch('hkopenai.hk_health_mcp_server.server.tool_specialist_waiting_time_by_cluster')
    @patch('hkopenai.hk_health_mcp_server.server.tool_pas_gopc_avg_quota')
    def test_create_mcp_server(self, mock_tool_pas_gopc_avg_quota, mock_tool_specialist_waiting_time_by_cluster, mock_tool_aed_waiting, mock_fastmcp):
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

        # Verify that the tool decorator was called for each tool function
        self.assertEqual(mock_server.tool.call_count, 3)

        # Get all decorated functions
        decorated_funcs = {call.args[0].__name__: call.args[0] for call in mock_server.tool.return_value.call_args_list}
        self.assertEqual(len(decorated_funcs), 3)

        # Call each decorated function and verify that the correct underlying function is called
        
        decorated_funcs['get_aed_waiting_times'](lang="en")
        mock_tool_aed_waiting.get_aed_waiting_times.assert_called_once_with("en")

        decorated_funcs['get_specialist_waiting_times'](lang="tc")
        mock_tool_specialist_waiting_time_by_cluster.get_specialist_waiting_times.assert_called_once_with("tc")

        decorated_funcs['get_pas_gopc_avg_quota'](lang="en", district="Tuen Mun")
        mock_tool_pas_gopc_avg_quota.get_pas_gopc_avg_quota.assert_called_once_with("en", "Tuen Mun")

if __name__ == "__main__":
    unittest.main()
