import atexit
from os import environ
import sentry_sdk

from sentry_sdk.integrations.flask import FlaskIntegration
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics
from sync_service.api.sync_stats import sync_stats, stats_sync_api
from sync_service.api.sync_user import sync_users, users_sync_api

metrics = PrometheusMetrics.for_app_factory()

sync_interval_seconds = 7200 # 2 Hours

if not environ.get('DB_BYPASS', None):
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=sync_stats, trigger="interval", seconds=sync_interval_seconds)
    scheduler.start()
    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())

def create_app():
    app = Flask(__name__)
    app.register_blueprint(users_sync_api, url_prefix='/api/syncservice/users')
    app.register_blueprint(stats_sync_api, url_prefix='/api/syncservice/stats')

    dsn = environ.get("SENTRY_DSN")
    sentry_sdk.init(
        dsn=dsn,
        integrations=[FlaskIntegration()],

        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=1.0
    )

    return app
    
def setup_metrics(app):
    metrics.init_app(app)
    return app

def main():
    app = create_app()
    app = setup_metrics(app)
    app.run(host='0.0.0.0', port = 5001, debug = False)