# markt-server ![build_staus](https://travis-ci.org/k-nut/markt-server.svg)

Server for filtering data for wo-ist-markt.de by opening hours.

Setup:
```
git clone git@github.com:k-nut/markt-server.git
cd markt-server
virtualenv .
source bin/activate
pip install -r requirements.txt
python app.py
```
Now you can make requests to [http://localhost:5000](http://localhost:5000) that filter by opening hours.

The only endpoint is `open_at` and needs to be passed parameters `city`, `day`, `time`.
An example cal would be: [http://localhost:5000/open_at?city=Berlin&day=su&time=18:00](http://localhost:5000/open_at?city=Berlin&day=su&time=18:00)

Note: The data was just once stolen from the upstream wo ist markt repository and must be updated manually on change.

This projects uses and includes a copy of [osm-opening-hours](https://github.com/martinfilliau/osm-opening-hours) as that is not available on pip.
