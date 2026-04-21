from flask import Flask, jsonify, request

from flask import Blueprint, jsonify, request

from flaskbook_api.api import calculation
# 공통의 prefix를 덧붙여 씀
api = Blueprint("api", __name__)



def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    return append

@api.get("/")
def index():
    return jsonify({"column": "value"}), 201

@api.post("/detect")
def detection():
    return calculation.detection(request)
