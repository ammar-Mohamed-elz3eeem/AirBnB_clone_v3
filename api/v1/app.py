#!/usr/bin/python3
"""Flask api for AirBnB"""
from models import storage
from api.v1.views import app_views
from os import getenv
from flask import Flask, jsonify


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(e):
    """close connection to storage engine"""
    if storage is not None:
        storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """page not found middleware for handling error pages"""
    return jsonify({
        "error": "Not found"
    }), 404


if __name__ == "__main__":
    app.run(
        threaded=True,
        host=getenv("HBNB_API_HOST", '0.0.0.0'),
        port=getenv("HBNB_API_PORT", 5000),
    )
