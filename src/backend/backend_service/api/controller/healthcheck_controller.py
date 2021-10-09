from http import HTTPStatus
import json
from flask import Blueprint, make_response, jsonify
from werkzeug.wrappers import response

healthcheck_api = Blueprint('healthcheck_api', __name__)

@healthcheck_api.route('/', methods=['GET'])
def healthcheck():
    """
    Healthcheck endpoint
    """

    response = {"status": 200, "message": "OK"}
    return make_response(response, HTTPStatus.OK)