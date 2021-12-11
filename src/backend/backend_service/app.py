from os import environ
import sentry_sdk

from flask import Flask
from sentry_sdk.integrations.flask import FlaskIntegration
from backend_service.api.controller.roll_controller import roll_api
from backend_service.api.controller.stats_controller import stats_api
from backend_service.api.controller.healthcheck_controller import healthcheck_api
from backend_service.api.controller.sentry_controller import sentry_api

def create_app():
    app = Flask(__name__)
    app.register_blueprint(roll_api, url_prefix='/api/backendservice/roll')
    app.register_blueprint(stats_api, url_prefix='/api/backendservice/stats')
    app.register_blueprint(healthcheck_api, url_prefix='/api/backendservice/healthcheck')
    app.register_blueprint(sentry_api, url_prefix="/api/backendservice/sentry")

    dsn = environ.get("SENTRY_DSN")
    sentry_sdk.init(
        dsn=dsn,
        integrations=[FlaskIntegration()],

        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=1.0
    )

    app.env = environ.get("ENV")

    return app

def main():
    app = create_app()
    app.run(host='0.0.0.0', port = 5000)