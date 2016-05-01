import pytest


from app import controller

def get_cities():
    return ["berlin"]

@pytest.fixture(autouse=True)
def mock_get_cities(monkeypatch):
    monkeypatch.setattr(controller, 'get_cities', get_cities)

@pytest.fixture(autouse=True)
def mock_get_data(monkeypatch):
    monkeypatch.setattr(controller, 'get_data_for', create_fake_data)

def create_fake_data(*args):
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

