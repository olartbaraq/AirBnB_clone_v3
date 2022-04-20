#!/usr/bin/python3
"""create a response form JSON file with the necessary modules"""
from flask import Flask, abort, jsonify, request
import json
from api.v1.views import app_views
from models.state import State
from models import storage



@app_views.route('/states', strict_slashes=False, methods=['GET'])
def to_retrieve():
    objects = storage.all('State')
    lista = []
    for state in objects.values():
        lista.append(state.to_dict())
    return jsonify(lista)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def get_state(state_id):
    """return the response status in form of json structure"""
    objects = storage.all('State')
    lista = []
    for state in objects.values():
        lista.append(state.to_dict())
    State = [state for state in lista if state['id'] == state_id]
    if len(State) == 0:
        abort(404)
    return jsonify(State[0]), '200'

@app_views.route('/states/<state_id>', strict_slashes=False, methods=['DELETE'])
def delete_state(state_id):
    """return the response status in form of json structure"""
    objects = storage.all('State')
    lista = []
    for state in objects.values():
        lista.append(state.to_dict())
    State = [state for state in lista if state['id'] == state_id]
    if len(State) == 0:
        abort(404)
    storage.delete(State)
    storage.save
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
    objects = storage.all('State')
    lista = []
    for state in objects.values():
        lista.append(state.to_dict())
    for state in lista:
        if state['id'] == state_id:
            State = state
    if len(State) == 0:
        abort(404)
        json.dumps(response)
    response = request.get_json()
    if response is None:
        abort(400, {'Not a JSON'})
    ignoreKeys = ['id', 'created_at', 'updated_at']
    for key, value in response.items():
        if key not in ignoreKeys:
            State[key] = value
    storage.save()
    return jsonify(State), '200'
