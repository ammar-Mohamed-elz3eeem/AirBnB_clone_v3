#!/usr/bin/python3
"""Flask api for AirBnB"""
from flask import Blueprint


app_views = Blueprint(
    name="app_views",
    import_name=__name__,
    url_prefix="/api/v1",
    template_folder="templates",
    static_folder="static"
)


if app_views is not None:
    from api.v1.views.index import *
    from api.v1.views.states import *
    from api.v1.views.cities import *
