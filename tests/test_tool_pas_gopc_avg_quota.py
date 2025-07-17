"""
Module for testing the general outpatient clinic quota data fetching functionality.
This module contains unit tests to verify the behavior of the quota data retrieval.
"""

import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
import json

from hkopenai.hk_health_mcp_server.tools.pas_gopc_avg_quota import (
    _get_pas_gopc_avg_quota,
    register,
)


class TestPasGopcAvgQuotaTool(unittest.TestCase):
    """
    Test class for verifying general outpatient clinic quota data fetching.
    This class contains tests to ensure the data retrieval functions correctly.
    """

    JSON_DATA = """[
        {
            "District": "Central & Western",
            "Clinic": "Central District Health Centre",
            "AvgQuota": "100"
        },
        {
            "District": "Tuen Mun",
            "Clinic": "Tuen Mun Clinic",
            "AvgQuota": "150"
        },
        {
            "District": "Tuen Mun",
            "Clinic": "Siu Lam Clinic",
            "AvgQuota": "50"
        }
    ]"""

    @patch("hkopenai.hk_health_mcp_server.tools.pas_gopc_avg_quota.fetch_json_data")
    def test_get_pas_gopc_avg_quota_all_districts(self, mock_fetch_json_data):
        """
        Test retrieval of general outpatient clinic quota data for all districts.
        Verifies that data for all districts is returned correctly.
        """
        mock_fetch_json_data.return_value = json.loads(self.JSON_DATA)
        with patch(
            "hkopenai.hk_health_mcp_server.tools.pas_gopc_avg_quota.datetime"
        ) as mock_datetime:
            mock_datetime.now.return_value = datetime(2025, 7, 14, 10, 0, 0)
            mock_datetime.isoformat.return_value = "2025-07-14T10:00:00"
            result = _get_pas_gopc_avg_quota(lang="en")
            mock_fetch_json_data.assert_called_once_with(
                "https://www.ha.org.hk/pas_gopc/pas_gopc_avg_quota_pdf/g0_9uo7a_p-en.json"
            )
            self.assertIn("data", result)
            self.assertIn("last_updated", result)
            self.assertEqual(len(result["data"]), 3)
            self.assertEqual(result["last_updated"], "2025-07-14T10:00:00")
            self.assertEqual(result["message"], "Retrieved data for 3 clinics")

    @patch("hkopenai.hk_health_mcp_server.tools.pas_gopc_avg_quota.fetch_json_data")
    def test_get_pas_gopc_avg_quota_filtered_by_district(self, mock_fetch_json_data):
        """
        Test retrieval of general outpatient clinic quota data filtered by district.
        Verifies that only data for the specified district is returned.
        """
        mock_fetch_json_data.return_value = json.loads(self.JSON_DATA)
        with patch(
            "hkopenai.hk_health_mcp_server.tools.pas_gopc_avg_quota.datetime"
        ) as mock_datetime:
            mock_datetime.now.return_value = datetime(2025, 7, 14, 10, 0, 0)
            mock_datetime.isoformat.return_value = "2025-07-14T10:00:00"
            result = _get_pas_gopc_avg_quota(lang="en", district="Tuen Mun")
            mock_fetch_json_data.assert_called_once_with(
                "https://www.ha.org.hk/pas_gopc/pas_gopc_avg_quota_pdf/g0_9uo7a_p-en.json"
            )
            self.assertIn("data", result)
            self.assertIn("last_updated", result)
            self.assertEqual(len(result["data"]), 2)
            self.assertEqual(result["data"][0]["District"], "Tuen Mun")
            self.assertEqual(result["data"][1]["District"], "Tuen Mun")
            self.assertEqual(result["last_updated"], "2025-07-14T10:00:00")
            self.assertEqual(result["message"], "Retrieved data for 2 clinics in Tuen Mun")

    @patch("hkopenai.hk_health_mcp_server.tools.pas_gopc_avg_quota.fetch_json_data")
    def test_get_pas_gopc_avg_quota_error_handling(self, mock_fetch_json_data):
        """
        Test error handling when fetching data.
        Verifies that an error message is returned when data fetching fails.
        """
        mock_fetch_json_data.return_value = {"error": "Network error"}
        result = _get_pas_gopc_avg_quota(lang="en")
        self.assertEqual(result, {"type": "Error", "error": "Network error"})

    def test_register_tool(self):
        """
        Test the registration of the get_pas_gopc_avg_quota tool.

        This test verifies that the register function correctly registers the tool
        with the FastMCP server and that the registered tool calls the underlying
        _get_pas_gopc_avg_quota function.
        """
        mock_mcp = MagicMock()

        # Call the register function
        register(mock_mcp)

        # Verify that mcp.tool was called with the correct description
        mock_mcp.tool.assert_called_once_with(
            description="Get average number of general outpatient clinic quotas for the preceding 4 weeks across 18 districts in Hong Kong"
        )

        # Get the mock that represents the decorator returned by mcp.tool
        mock_decorator = mock_mcp.tool.return_value

        # Verify that the mock decorator was called once (i.e., the function was decorated)
        mock_decorator.assert_called_once()

        # The decorated function is the first argument of the first call to the mock_decorator
        decorated_function = mock_decorator.call_args[0][0]

        # Verify the name of the decorated function
        self.assertEqual(decorated_function.__name__, "get_pas_gopc_avg_quota")

        # Call the decorated function and verify it calls _get_pas_gopc_avg_quota
        with patch(
            "hkopenai.hk_health_mcp_server.tools.pas_gopc_avg_quota._get_pas_gopc_avg_quota"
        ) as mock_get_pas_gopc_avg_quota:
            decorated_function(lang="en", district="Tuen Mun")
            mock_get_pas_gopc_avg_quota.assert_called_once_with("en", "Tuen Mun")

if __name__ == "__main__":
    unittest.main()
