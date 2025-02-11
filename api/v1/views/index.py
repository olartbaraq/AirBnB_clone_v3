#!/usr/bin/python3
"""create a response form JSON file with the necessary modules"""

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.user import User
from models.review import Review


@app_views.route('/status', strict_slashes=False)
def return_response():
    """return the response status in form of json structure"""
    return jsonify(status="OK")


@app_views.route('/stats', strict_slashes=False)
def ret_number():
    """JSON structure response"""
    count = {}
    count["amenities"] = storage.count('Amenity')
    count["cities"] = storage.count('City')
    count["places"] = storage.count('Place')
    count["reviews"] = storage.count('Review')
    count["states"] = storage.count('State')
    count["users"] = storage.count('User')
    return jsonify(count)
