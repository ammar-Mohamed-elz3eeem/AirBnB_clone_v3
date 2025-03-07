#!/usr/bin/python3
"""users"""
from api.v1.app import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route("/users", strict_slashes=False)
def get_users():
    """ get all users """
    users = storage.all(User)
    return jsonify([user.to_dict() for user in users.values()])


@app_views.route("/users/<string:user_id>", strict_slashes=False)
def get_user(user_id):
    """ get user by id """
    user = storage.get(User, user_id)
    if user is None:
        return abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<string:user_id>", strict_slashes=False,
                 methods=["DELETE"])
def delete_user(user_id):
    """ delete user by id """
    user = storage.get(User, user_id)
    if user is None:
        return abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({})


@app_views.route("/users", strict_slashes=False, methods=["POST"])
def add_user():
    data = request.get_json()
    if not isinstance(data, dict):
        return abort(400, "Not a JSON")
    if data.get("email") is None:
        return abort(400, "Missing email")
    if data.get("password") is None:
        return abort(400, "Missing password")
    user = User(**data)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route("/users/<string:user_id>", strict_slashes=False,
                 methods=["PUT"])
def update_user(user_id):
    user = storage.get(User, user_id)
    if user is None:
        return abort(404)
    data = request.get_json()
    if not isinstance(data, dict):
        return abort(400, "Not a JSON")
    for (key, val) in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(user, key, val)
    user.save()
    return jsonify({**user})
