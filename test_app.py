import unittest
import json

import app

class FlaskrTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.app.test_client()
        app.app.config['TESTING'] = True

    def test_routes_shows_available_routes(self):
        response = self.app.get('/routes')
        assert response.status_code == 200
        response = json.loads(response.data)
        assert "open_at" in response["routes"]
        assert "city" in response["routes"]["open_at"]["params"]
        assert "time" in response["routes"]["open_at"]["params"]
        assert "day" in response["routes"]["open_at"]["params"]

    def test_city_does_not_exist(self):
        response = self.app.get('/open_at?city=Hamburg')
        assert response.status_code == 404
        response = json.loads(response.data)
        assert "not found" in response["message"]

    def test_returns_all_data_for_city_that_exsist(self):
        response = self.app.get('/open_at?city=Berlin')
        assert response.status_code == 200
        response = json.loads(response.data)
        assert len(response["features"]) == 2

    def test_validates_day_parameter(self):
        response = self.app.get('/open_at?city=Berlin&day=no&time=12:00')
        assert response.status_code == 400
        response = json.loads(response.data)
        expected_message = "Parameter day must be one of ['mo', 'tu', 'we', 'th', 'fr', 'sa', 'su']"
        assert response["message"] == expected_message

    def test_open_at_filters_by_opening_hours(self):
        response = self.app.get('/open_at?city=Berlin&day=mo&time=14:00')
        assert response.status_code == 200
        response = json.loads(response.data)
        assert len(response["features"]) == 1
