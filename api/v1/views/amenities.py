#!/usr/bin/python3
""" amenties routes for reading, updating, creating, deleteing amenties """
from api.v1.app import app_views
from models.amenity import Amenity
from models import storage
from flask import jsonify, request, abort, Response
import json


@app_views.route("/amenities", strict_slashes=False)
def get_amenities():
    """get all amenities from our storage engine"""
    objs = storage.all(Amenity)
    objs = [obj.to_dict() for obj in objs.values()]
    return jsonify(objs)


@app_views.route("/amenities/<string:amenity_id>", strict_slashes=False)
def get_amenity(amenity_id):
    """get state based on amenity_id"""
    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(obj.to_dict())


@app_views.route("/amenities", strict_slashes=False, methods=['POST'])
def add_amenity():
    """add new amenity route"""
    obj = request.get_json()
    if not isinstance(obj, dict):
        return abort(Response("Not a JSON", 400))
    if obj.get("name") is None:
        return abort(Response("Missing name", 400))
    amenity = Amenity(**obj)
    storage.new(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route("/amenities/<string:amenity_id>", methods=["DELETE"])
def delete_amenity(amenity_id):
    """delete amenity route"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return abort(404)
    amenity.delete()
    storage.save()
    return jsonify({})


@app_views.route("/amenities/<string:amenity_id>", methods=["PUT"])
def update_amenity(amenity_id):
    """update amenity route"""
    obj = request.get_json()
    if not isinstance(obj, dict):
        return abort(Response("Not a JSON", 400))
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return abort(404)
    for k, v in obj.items():
        if k not in ["id", "created_at", "updated_at"]:
            setattr(amenity, k, v)
    amenity.save()
    return jsonify(amenity.to_dict())
