import unittest
import json

from mock import patch

import app

def create_fake_data():
    return {
        "features": [
            {
                "geometry": {
                    "coordinates": [
                        13.062124,
                        52.401653
                    ],
                    "type": "Point"
                },
                "properties": {
                    "title": "Wochenmarkt Potsdam Bassinplatz",
                    "location": "Wochenmarkt Potsdam Bassinplatz",
                    "opening_hours": "Mo-Fr 07:00-16:00;Sa 07:00-13:00",
                },
                "type": "Feature"
            },
            {
                "geometry": {
                    "coordinates": [
                        13.095129,
                        52.3942
                    ],
                    "type": "Point"
                },
                "properties": {
                    "title": "Floh- und Bauernmarkt in Potsdam Weberplatz, 14482 Potsdam",
                    "location": "Floh- und Bauernmarkt in Potsdam Weberplatz, 14482 Potsdam",
                    "opening_hours": "Sa 07:00-13:00",
                },
                "type": "Feature"
            }
        ]
    }

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

    @patch("app.controller.get_cities", return_value=["berlin"])
    def test_city_does_not_exist(self, mock_get_cities):
        response = self.app.get('/open_at?city=Hamburg')
        assert response.status_code == 404
        response = json.loads(response.data)
        assert "not found" in response["message"]

    @patch("app.controller.get_cities", return_value=["berlin"])
    @patch("app.controller.get_data_for", return_value=create_fake_data())
    def test_returns_all_data_for_city_that_exsist(self, mock_get_data_for, mock_get_cities):
        response = self.app.get('/open_at?city=Berlin')
        assert response.status_code == 200
        response = json.loads(response.data)
        assert len(response["features"]) == 2

    @patch("app.controller.get_cities", return_value=["berlin"])
    @patch("app.controller.get_data_for", return_value=create_fake_data())
    def test_validates_day_parameter(self, mock_get_data_for, mock_get_cities):
        response = self.app.get('/open_at?city=Berlin&day=no&time=12:00')
        assert response.status_code == 400
        response = json.loads(response.data)
        assert response["message"] == "Parameter day must be one of ['mo', 'tu', 'we', 'th', 'fr', 'sa', 'su']"

    @patch("app.controller.get_cities", return_value=["berlin"])
    @patch("app.controller.get_data_for", return_value=create_fake_data())
    def test_open_at_filters_by_opening_hours(self, mock_get_data_for, mock_get_cities):
        response = self.app.get('/open_at?city=Berlin&day=mo&time=14:00')
        assert response.status_code == 200
        response = json.loads(response.data)
        assert len(response["features"]) == 1
