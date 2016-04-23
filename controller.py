import os
import json

from flask import jsonify

from osm_time.opening_hours import OpeningHours



def get_cities():
    filenames = [f for f in os.listdir("./data") if os.path.isfile(os.path.join("./data", f))]
    cities = [filename.split(".")[0] for filename in filenames]
    return cities


def get_data_for(city):
    filename = "%s.json" % city.lower()
    path = os.path.join("./data", filename)
    with open(path) as infile:
        data = json.load(infile)
        return data


def filter_by(features, day, time):
    filtered = []
    for city in features:
        opening_hours = city["properties"].get("opening_hours")
        if opening_hours is None:
            continue
        openings = OpeningHours(opening_hours)
        if openings.is_open(day, time):
            filtered.append(city)
    return filtered


def get_routes():
    routes = {"routes":
                {"open_at":
                    {"params": ["day", "time", "city"]},
                 "routes":
                    {"params": []}
                }
             }
    return jsonify(routes)
