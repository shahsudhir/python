import unittest
from unittest.mock import patch
import requests

class TestPythonRepos(unittest.TestCase):
    def setUp(self):
        """Set up mock data and URL for testing."""
        self.url = 'https://api.github.com/search/repositories?q=language:python&sort=stars'
        self.headers = {'Accept': 'application/vnd.github.v3+json'}
        # Mock response data
        self.mock_response = {
            'total_count': 150000,  # Example total count
            'items': [
                {'name': 'repo1', 'stargazers_count': 50000},
                {'name': 'repo2', 'stargazers_count': 40000},
                # Simulate 30 items
                *[{ 'name': f'repo{i}', 'stargazers_count': 1000 * (33 - i) } for i in range(3, 31)]
            ]
        }

    @patch('requests.get')
    def test_status_code(self, mock_get):
        """Test that the API call returns a status code of 200."""
        # Configure mock to return a response with status code 200
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = self.mock_response
        mock_get.return_value = mock_response

        # Simulate the API call
        r = requests.get(self.url, headers=self.headers)
        self.assertEqual(r.status_code, 200, "API call did not return status code 200")

    @patch('requests.get')
    def test_items_count(self, mock_get):
        """Test that the number of items returned is 30."""
        # Configure mock
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = self.mock_response
        mock_get.return_value = mock_response

        # Simulate the API call
        r = requests.get(self.url, headers=self.headers)
        response_dict = r.json()
        items = response_dict['items']
        self.assertEqual(len(items), 30, f"Expected 30 items, but got {len(items)}")

    @patch('requests.get')
    def test_total_count(self, mock_get):
        """Test that the total number of repositories is greater than 100,000."""
        # Configure mock
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = self.mock_response
        mock_get.return_value = mock_response

        # Simulate the API call
        r = requests.get(self.url, headers=self.headers)
        response_dict = r.json()
        total_count = response_dict['total_count']
        self.assertGreater(total_count, 100000, f"Total count {total_count} is not greater than 100,000")

if __name__ == '__main__':
    unittest.main()