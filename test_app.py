import unittest
from mock import patch
import json

import app

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.app.test_client()

    @patch("app.get_cities", return_value=["berlin"])
    def test_city_does_not_exist(self, mock_get_cities):
        rv = self.app.get('/open_at?city=Hamburg')
        print rv.data
        response = json.loads(rv.data)
        assert "not found" in response["message"]
