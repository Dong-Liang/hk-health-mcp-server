"""
Module for testing the AED waiting times data fetching functionality.
This module contains unit tests to verify the behavior of the AED data retrieval.
"""

import unittest
from unittest.mock import patch, mock_open
from hkopenai.hk_health_mcp_server.tool_aed_waiting import fetch_aed_waiting_data
import json


class TestAEDWaitingTimes(unittest.TestCase):
    """
    Test class for verifying AED waiting times data fetching.
    This class contains tests to ensure the data retrieval functions correctly.
    """
    JSON_DATA = """{
    "waitTime": [
      {
        "hospName": "Alice Ho Miu Ling Nethersole Hospital",
        "topWait": "Over 4 hours"
      },
      {
        "hospName": "Caritas Medical Centre",
        "topWait": "Over 1 hour"
      },
      {
        "hospName": "Kwong Wah Hospital",
        "topWait": "Around 1 hour"
      }
    ],
    "updateTime": "10/6/2025 9:45pm"
  }"""

    def setUp(self):
        self.mock_urlopen = patch("urllib.request.urlopen").start()
        self.mock_urlopen.return_value = mock_open(
            read_data=self.JSON_DATA.encode("utf-8")
        )()
        self.addCleanup(patch.stopall)

    @patch("urllib.request.urlopen")
    def test_fetch_aed_waiting_data(self, mock_urlopen):
        """
        Test the fetching of AED waiting time data.
        Verifies that the data is correctly retrieved and parsed from the mocked response.
        """
        # Mock the URL response
        mock_urlopen.return_value = mock_open(
            read_data=self.JSON_DATA.encode("utf-8")
        )()

        # Call the function
        result = fetch_aed_waiting_data()

        # Verify the result
        self.assertIsInstance(result, dict)
        self.assertIn("waitTime", result)
        self.assertIn("updateTime", result)
        self.assertEqual(len(result["waitTime"]), 3)
        self.assertEqual(
            result["waitTime"][0]["hospName"], "Alice Ho Miu Ling Nethersole Hospital"
        )
        self.assertEqual(result["waitTime"][0]["topWait"], "Over 4 hours")
        self.assertEqual(result["updateTime"], "10/6/2025 9:45pm")


if __name__ == "__main__":
    unittest.main()
