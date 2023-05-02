#!/usr/bin/python3
"""Flask api for AirBnB"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status")
def status_route():
    return jsonify({"status": "OK"})
