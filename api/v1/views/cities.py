#!/usr/bin/python3
"""cities"""

from api.v1.app import app_views
from models.state import State
from models.city import City
from models import storage
from flask import jsonify, abort, request, Response


@app_views.route("/states/<string:state_id>/cities", strict_slashes=False)
def get_cities(state_id):
    """get cities of state with state_id"""
    state = storage.get(State, state_id)
    if state is None:
        return abort(404)
    return jsonify(list(map(lambda city: city.to_dict(), state.cities)))


@app_views.route("/cities/<city_id>", strict_slashes=False)
def get_city(city_id):
    """get city from its id"""
    city = storage.get(City, city_id)
    print(city)
    if city is None:
        return abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=["DELETE"])
def delete_city(city_id):
    """delete the city with id city_id"""
    city = storage.get(City, city_id)
    if city is None:
        return abort(404)
    city.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/<string:state_id>/cities",
                 strict_slashes=False, methods=["POST"])
def create_city(state_id):
    """create new city in specefiec state"""
    data = request.get_json()
    state = storage.get(State, state_id)
    if state is None:
        return abort(404)
    if not isinstance(data, dict):
        return abort(Response("Not a JSON0", 400))
    if data.get("name") is None:
        return abort(Response("Missing name", 400))
    city = City(**data, state_id=state_id)
    storage.new(state)
    return jsonify(city.to_dict()), 201


@app_views.route("/cities/<string:city_id>",
                 strict_slashes=False, methods=["PUT"])
def update_city(city_id):
    """update city using its id"""
    city = storage.get(City, city_id)
    if city is None:
        return abort(404)
    data = request.get_json()
    if not isinstance(data, dict):
        return abort(Response("Not a JSON", 400))
    for (k, v) in data.items():
        if k not in ["id", "created_at", "updated_at"]:
            setattr(city, k, v)
    city.save()
    return jsonify(city.to_dict()), 200
