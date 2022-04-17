#!/usr/bin/python3
"""import necessary modules"""

from flask import Flask, abort, jsonify, request
import json
from api.v1.views import app_views
from os import name
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def to_retrieve():
    """to retrieve state objects"""
    objects = storage.all('State')
    lista = []
    for state in objects.values():
        lista.append(state.to_dict())
    return jsonify(lista)


@app_views.route('/states/<state_id>', methods=['GET'],
                 strict_slashes=False)
def to_retrieve_id(state_id):
    '''retrieves a State object id'''
    try:
        objects = storage.all(State)['State.{}'.format(state_id)]
    except(KeyError):
        abort(404)
    if not objects:
        abort(404)
    return jsonify(objects.to_dict()), 'OK'


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def deleting(state_id):
    ''' to delete an onbject'''
    stateObject = storage.all(State)['State.{}'.format(state_id)]
    if not stateObject:
        abort(404)
    storage.delete(stateObject)
    storage.save()
    return jsonify({}), '200'


@app_views.route('/states', methods=['POST'],
                 strict_slashes=False)
def creates_a_state():
    """creates a state"""
    response = request.get_json()
    if response is None:
        abort(400, {'Not a JSON'})
    if "name" not in response:
        abort(400, {'Missing name'})
    stateObject = State(name=response['name'])
    storage.new(stateObject)
    storage.save()
    return jsonify(stateObject.to_dict()), '201'


@app_views.route('/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def updates_states(state_id):
    """updates a states object with put request"""
    response = request.get_json()
    if response is None:
        abort(400, {'Not a JSON'})
    stateObject = storage.all(State)["State.{}".format(state_id)]
    if stateObject is None:
        abort(404)
        json.dumps(response)
    ignoreKeys = ['id', 'created_at', 'updated_at']
    for key, value in response.items():
        if key not in ignoreKeys:
            setattr(stateObject, key, value)
    storage.save()
    return jsonify(stateObject.to_dict()), '200'
