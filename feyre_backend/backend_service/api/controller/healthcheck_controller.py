from flask import Blueprint

healthcheck_api = Blueprint('healthcheck_api', __name__)

@healthcheck_api.route('/', methods=['GET'])
def healthcheck():
    """
    Healthcheck endpoint
    """

    return "OK"
