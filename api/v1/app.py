#!/usr/bin/python3
""" import necesaary modules for variable app.py"""
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from os import getenv
from api.v1.views import app_views


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)
app.url_map.strict_slaches = False


@app.teardown_appcontext
def call_storage(exception=None):
    """method to call storage.close()"""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """return error page in json"""
    return jsonify(error="Not found"), '404'


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST')
    port = getenv('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, threaded=True)
