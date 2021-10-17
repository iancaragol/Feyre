from http import HTTPStatus
import json
from flask import Blueprint, make_response, jsonify
from werkzeug.wrappers import response
from common.redis_helper import RedisHelper

healthcheck_api = Blueprint('healthcheck_api', __name__)
redis_helper = RedisHelper()

@healthcheck_api.route('/', methods=['GET'])
def healthcheck():
    """
    Healthcheck endpoint
    """

    response = {
        "status": 200,
        "message": "OK",
        "backend" : "Healthy",
        "redis" : redis_helper.get_redis_health()
    }
    return make_response(response, HTTPStatus.OK)