import unittest
import unittest.mock as mock
from unittest.mock import patch
import requests
from hkopenai.hk_health_mcp_server import tool_pas_gopc_avg_quota

class TestPasGopcAvgQuotaTool(unittest.TestCase):
    @patch('requests.get')
    def test_fetch_pas_gopc_avg_quota_data(self, mock_get):
        # Setup mock response
        mock_response = mock.Mock()
        mock_response.json.return_value = [
            {"Period": {"from": "20250518", "to": "20250614"}, "District": "Tuen Mun", "Clinic": "TUEN MUN CLINIC", "Doctor Consultation Sessions": "Mon to Fri (AM, PM and Evening) Sat (AM), Sun (AM) and Public Holiday", "Monday": "469.0", "Tuesday": "464.5", "Wednesday": "434.5", "Thursday": "434.8", "Friday": "435.0", "Saturday": "114.3", "Sunday": "95.0"}
        ]
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Test fetching data
        data = tool_pas_gopc_avg_quota.fetch_pas_gopc_avg_quota_data(lang="en")
        
        # Verify the call and results
        mock_get.assert_called_once_with("https://www.ha.org.hk/pas_gopc/pas_gopc_avg_quota_pdf/g0_9uo7a_p-en.json")
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["District"], "Tuen Mun")

    def test_get_pas_gopc_avg_quota_all_districts(self):
        # Mock fetch_pas_gopc_avg_quota_data
        with patch.object(tool_pas_gopc_avg_quota, 'fetch_pas_gopc_avg_quota_data') as mock_fetch:
            mock_fetch.return_value = [
                {"Period": {"from": "20250518", "to": "20250614"}, "District": "Tuen Mun", "Clinic": "TUEN MUN CLINIC", "Doctor Consultation Sessions": "Mon to Fri (AM, PM and Evening) Sat (AM), Sun (AM) and Public Holiday", "Monday": "469.0", "Tuesday": "464.5", "Wednesday": "434.5", "Thursday": "434.8", "Friday": "435.0", "Saturday": "114.3", "Sunday": "95.0"},
                {"Period": {"from": "20250518", "to": "20250614"}, "District": "Shatin", "Clinic": "SHATIN (TAI WAI) GOPC", "Doctor Consultation Sessions": "Mon to Fri (AM and PM) Sat (AM)", "Monday": "129.8", "Tuesday": "129.3", "Wednesday": "128.3", "Thursday": "190.8", "Friday": "190.3", "Saturday": "111.3", "Sunday": "N/A"}
            ]
            
            # Test getting data for all districts
            result = tool_pas_gopc_avg_quota.get_pas_gopc_avg_quota(lang="en")
            
            # Verify results
            self.assertEqual(len(result['data']), 2)
            self.assertIn('last_updated', result)
            self.assertEqual(result['message'], "Retrieved data for 2 clinics")

    def test_get_pas_gopc_avg_quota_filtered_district(self):
        # Mock fetch_pas_gopc_avg_quota_data
        with patch.object(tool_pas_gopc_avg_quota, 'fetch_pas_gopc_avg_quota_data') as mock_fetch:
            mock_fetch.return_value = [
                {"Period": {"from": "20250518", "to": "20250614"}, "District": "Tuen Mun", "Clinic": "TUEN MUN CLINIC", "Doctor Consultation Sessions": "Mon to Fri (AM, PM and Evening) Sat (AM), Sun (AM) and Public Holiday", "Monday": "469.0", "Tuesday": "464.5", "Wednesday": "434.5", "Thursday": "434.8", "Friday": "435.0", "Saturday": "114.3", "Sunday": "95.0"},
                {"Period": {"from": "20250518", "to": "20250614"}, "District": "Shatin", "Clinic": "SHATIN (TAI WAI) GOPC", "Doctor Consultation Sessions": "Mon to Fri (AM and PM) Sat (AM)", "Monday": "129.8", "Tuesday": "129.3", "Wednesday": "128.3", "Thursday": "190.8", "Friday": "190.3", "Saturday": "111.3", "Sunday": "N/A"}
            ]
            
            # Test getting data for a specific district
            result = tool_pas_gopc_avg_quota.get_pas_gopc_avg_quota(lang="en", district="Tuen Mun")
            
            # Verify results
            self.assertEqual(len(result['data']), 1)
            self.assertEqual(result['data'][0]['District'], "Tuen Mun")
            self.assertIn('last_updated', result)
            self.assertEqual(result['message'], "Retrieved data for 1 clinics in Tuen Mun")

if __name__ == "__main__":
    unittest.main()
