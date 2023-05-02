#!/usr/bin/python3
"""Flask api for AirBnB"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.user import User
from models.place import Place
from models.city import City
from models.review import Review
from models.state import State


classes = {
  "amenities": Amenity,
  "cities": City,
  "places": Place,
  "reviews": Review,
  "states": State,
  "users": User
}


@app_views.route("/status", strict_slashes=False)
def status_route():
    """show json object with status OK"""
    return jsonify({"status": "OK"})


@app_views.route("/stats", strict_slashes=False)
def stats_route():
    return jsonify(dict([[k, storage.count(v)] for (k, v) in classes.items()]))
