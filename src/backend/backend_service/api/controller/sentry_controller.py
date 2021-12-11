from flask import Blueprint

sentry_api = Blueprint('sentry_api', __name__)

@sentry_api.route('/debug', methods=['GET'])
def trigger_error():
    division_by_zero = 1 / 0