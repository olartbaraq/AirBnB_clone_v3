#!/usr/bin/python3
""" API view for City objects. """
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
import json
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False, methods=['GET'])
def find_cities(state_id):
    """retrieves cities id from state"""
    cities = []
    city_objects = storage.all(City)
    for city in (city_objects).values():
        if state_id == city.state_id:
            cities.append(city.to_dict())
            return jsonify(cities)
    abort(404)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['GET'])
def get_city(city_id):
    """ Returns the City obj in JSON """
    city_objects = storage.all(City)
    for city in city_objects.values():
        if city_id == city.id:
            return jsonify(city.to_dict())
    abort(404)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['DELETE'])
def delete_city(city_id):
    """Deletes the city obj in the list"""
    city_objects = storage.all(City)
    for city in city_objects.values():
        if city_id == city.id:
            city.delete()
            storage.save()
            return (jsonify({})), '200'
    abort(404)


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['POST'])
def creates_city(state_id):
    """Creates the city obj to the state"""
    try:
        state_objs = storage.all(State)
    except (TypeError, KeyError):
        abort(404)
    if not state_objs:
        abort(404)
    content = request.get_json()
    try:
        json.dumps(content)
        if 'name' not in content:
            abort(400, {'message': 'Missing name'})
    except (TypeError, OverflowError):
        abort(400, {'message': 'Not a JSON'})
    content['state_id'] = state_id
    new_city = City(**content)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['PUT'])
def update_city(city_id):
    """ Updates a City obj to Storage. """
    dic = storage.all('City')
    for key in dic:
        if city_id == dic[key].id:
            if not request.json:
                return (jsonify("Not a JSON"), 400)
            else:
                forbidden = ["id", "update_at", "created_at", "state_id"]
                content = request.get_json()
                for k in content:
                    if k not in forbidden:
                        setattr(dic[key], k, content[k])
                dic[key].save()
                return jsonify(dic[key].to_dict())
    abort(404)
