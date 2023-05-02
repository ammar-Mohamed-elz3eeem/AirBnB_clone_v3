#!/usr/bin/python3
"""Flask api for AirBnB"""
from flask import Flask, Blueprint


app_views = Blueprint(
    name="app_views",
    import_name=__name__,
    url_prefix="/api/v1",
    template_folder="templates",
    static_folder="static"
)
