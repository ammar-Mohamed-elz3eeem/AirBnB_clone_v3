#!/usr/bin/python3
"""state routes for reading, updating, creating, deleteing states
from our storage engine"""
from api.v1.app import app_views
from models.state import State
from models import storage
from flask import jsonify, request, abort, Response
import json


@app_views.route("/states", strict_slashes=False)
def get_states():
    """get all states from our storage engine"""
    objs = storage.all(State)
    objs = [obj.to_dict() for obj in objs.values()]
    return jsonify(objs)


@app_views.route("/states/<string:state_id>", strict_slashes=False)
def get_state(state_id):
    """get state based on state_id"""
    obj = storage.get(State, state_id)
    if obj is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(obj.to_dict())


@app_views.route("/states", strict_slashes=False, methods=['POST'])
def add_state():
    """add new state route"""
    obj = request.get_json()
    print(obj)
    if not isinstance(obj, dict):
        return abort(Response("Not a JSON", 400))
    if obj.get("name") is None:
        return abort(Response("Missing name", 400))
    state = State(**obj)
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201


@app_views.route("/states/<string:state_id>", methods=["DELETE"])
def delete_state(state_id):
    """delete state route"""
    state = storage.get(State, state_id)
    if state is None:
        return abort(404)
    state.delete()
    storage.save()
    return jsonify({})


@app_views.route("/states/<string:state_id>", methods=["PUT"])
def update_state(state_id):
    """update state route"""
    obj = request.get_json()
    if not isinstance(obj, dict):
        return abort(Response("Not a JSON", 400))
    state = storage.get(State, state_id)
    if state is None:
        return abort(404)
    for k, v in obj.items():
        if k not in ["id", "created_at", "updated_at"]:
            setattr(state, k, v)
    state.save()
    return jsonify(state.to_dict())
