#/usr/bin/env python3
import os
from os import listdir
from os.path import isfile, join

from flask import Flask, request, jsonify
app = Flask(__name__)

def get_cities():
    filenames = [f for f in os.listdir("./data") if os.path.isfile(os.path.join("./data", f))]
    cities = [filename.split(".")[0] for filename in filenames]
    return cities

@app.route('/open_at')
def open_at():
    cities = get_cities
    city = request.args.get('city', None)
    if city is None or city.lower() not in cities:
        return jsonify({"message": "city %s not found" % city})
    return 'Hello World!'

if __name__ == '__main__':
    app.debug = True
    app.run()

