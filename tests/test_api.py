import unittest
from src.api.client import get_data

class TestAPI(unittest.TestCase):
    def test_get_data(self):
        # This is a placeholder test. Replace with a real API endpoint for actual testing.
        try:
            get_data('https://jsonplaceholder.typicode.com/todos/1')
        except Exception as e:
            self.fail(f"API call failed: {e}")

if __name__ == "__main__":
    unittest.main()
