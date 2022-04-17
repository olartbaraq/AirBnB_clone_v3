#!/usr/bin/python3
"""create a response form JSON file with the necessary modules"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def return_response():
    """return the response status in form of json structure"""
    return jsonify(status="OK")


@app_views.route('/stats', strict_slashes=False)
def ret_number():
    """JSON structure response"""
    count = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(count)
