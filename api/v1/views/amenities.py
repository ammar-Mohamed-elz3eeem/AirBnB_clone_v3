#!/usr/bin/python3
"""define all Amenties routes"""

from api.v1.app import app_views
from models.amenity import Amenity
from models import storage
from flask import jsonify, abort, request, Response


@app_views.route("/amenities", strict_slashes=False)
def get_amenities():
    """get all amenties"""
    amenties = storage.all(Amenity)
    return jsonify(list(map(lambda amenity: amenity.to_dict(), amenties)))


@app_views.route("/amenities/<amenity_id>", strict_slashes=False)
def get_amenity(amenity_id):
    """get amenity from its id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return abort(404)
    return jsonify(amenity.to_dict())


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=["DELETE"])
def delete_amenity(amenity_id):
    """delete the amenity with id amenity_id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return abort(404)
    amenity.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/amenities", strict_slashes=False, methods=["POST"])
def create_amenity(amenity_id):
    """create new amenity in specefiec amenity"""
    data = request.get_json()
    if not isinstance(data, dict):
        return abort(Response("Not a JSON", 400))
    if data.get("name") is None:
        return abort(Response("Missing name", 400))
    amenity = Amenity(**data)
    storage.new(amenity)
    return jsonify(amenity.to_dict()), 201


@app_views.route("/amenities/<string:amenity_id>",
                 strict_slashes=False, methods=["PUT"])
def update_amenity(amenity_id):
    """update amenity using its id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return abort(404)
    data = request.get_json()
    if not isinstance(data, dict):
        return abort(Response("Not a JSON", 400))
    for (k, v) in data.items():
        if k not in ["id", "created_at", "updated_at"]:
            setattr(amenity, k, v)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
