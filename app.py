#/usr/bin/env python3
""" The main app. It contains all the routes """
import json

from flask import Flask, request, jsonify

import controller

app = Flask(__name__)  # pylint: disable=invalid-name

@app.route('/routes')
def get_routes():
    """ Returns a list of api endpoints """
    return controller.get_routes()

@app.route('/open_at')
def open_at():
    """ Returns a geojson representation of markets that are open at
        the given date and time for the given city """
    cities = controller.get_cities()
    city = request.args.get('city', None)
    if (city is None) or (city.lower() not in cities):
        return json.dumps({"message": "city %s not found" % city}), 404
    else:
        data = controller.get_data_for(city)

    day = request.args.get("day", None)
    time = request.args.get("time", None)

    if day is not None and time is not None:
        days = ["mo", "tu", "we", "th", "fr", "sa", "su"]
        if day not in days:
            message = "Parameter day must be one of " + str(days)
            return json.dumps({"message": message}), 400
        data["features"] = controller.filter_by(data["features"], day, time)

    return jsonify(data)

if __name__ == '__main__':
    app.debug = True
    app.run()

