import unittest
import unittest.mock as mock
from unittest.mock import patch
from hkopenai.hk_health_mcp_server.server import create_mcp_server

class TestApp(unittest.TestCase):
    @patch('hkopenai.hk_health_mcp_server.server.FastMCP')
    @patch('hkopenai.hk_health_mcp_server.server.tool_aed_waiting')
    @patch('hkopenai.hk_health_mcp_server.server.tool_specialist_waiting_time_by_cluster')
    @patch('hkopenai.hk_health_mcp_server.server.tool_pas_gopc_avg_quota')
    def test_create_mcp_server(self, mock_tool_quota, mock_tool_specialist, mock_tool_aed, mock_fastmcp):
        # Setup mocks
        mock_server = mock.Mock()
        
        # Track decorator calls and capture decorated functions
        decorator_calls = []
        decorated_funcs = []
        
        def tool_decorator(description=None):
            # First call: @tool(description=...)
            decorator_calls.append(((), {'description': description}))
            
            def decorator(f):
                # Second call: decorator(function)
                nonlocal decorated_funcs
                decorated_funcs.append(f)
                return f
                
            return decorator
            
        mock_server.tool = tool_decorator
        mock_server.tool.call_args = None  # Initialize call_args
        mock_fastmcp.return_value = mock_server
        mock_tool_aed.get_aed_waiting_times.return_value = {'test': 'data'}
        mock_tool_specialist.get_specialist_waiting_times.return_value = {'data': [], 'last_updated': '2023-01-01T00:00:00'}
        mock_tool_quota.get_pas_gopc_avg_quota.return_value = {'data': [], 'last_updated': '2023-01-01T00:00:00', 'message': 'Retrieved data for 0 clinics'}

        # Test server creation
        server = create_mcp_server()

        # Verify server creation
        mock_fastmcp.assert_called_once()
        self.assertEqual(server, mock_server)

        # Verify tools were decorated
        self.assertEqual(len(decorated_funcs), 3)
        
        # Test the actual decorated functions
        for func in decorated_funcs:
            if 'aed' in func.__name__:
                result = func(lang="test")
                mock_tool_aed.get_aed_waiting_times.assert_called_with("test")
            elif 'specialist' in func.__name__:
                result = func(lang="test")
                mock_tool_specialist.get_specialist_waiting_times.assert_called_with("test")
            elif 'quota' in func.__name__:
                result = func(lang="test", district="")
                mock_tool_quota.get_pas_gopc_avg_quota.assert_called_with("test", "")
        
        # Verify tool descriptions were passed to decorator
        self.assertEqual(len(decorator_calls), 3)
        for call in decorator_calls:
            self.assertIsNotNone(call[1]['description'])

if __name__ == "__main__":
    unittest.main()
