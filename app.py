#/usr/bin/env python3
import os
import json

from flask import Flask, request, jsonify

from osm_time.opening_hours import OpeningHours

app = Flask(__name__)


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

@app.route('/open_at')
def open_at():
    cities = get_cities()
    city = request.args.get('city', None)
    if (city is None) or (city.lower() not in cities):
        return json.dumps({"message": "city %s not found" % city}), 404
    else:
        data = get_data_for(city)

    day = request.args.get("day", None)
    time = request.args.get("time", None)

    if day is not None and time is not None:
        if day not in ["mo", "tu", "we", "th", "fr", "sa", "su"]:
            return json.dumps({"message":"Parameter day must be one of [mo, tu, we, th, fr, sa, su]"}), 400
        data["features"] = filter_by(data["features"], day, time)

    return jsonify(data)

if __name__ == '__main__':
    app.debug = True
    app.run()

