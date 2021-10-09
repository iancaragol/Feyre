import atexit

from flask import Flask
from sync_service.api.sync_user import users_sync_api, sync_users
from sync_service.api.sync_stats import stats_sync_api
from apscheduler.schedulers.background import BackgroundScheduler

sync_interval_seconds = 7200 # 2 Hours
scheduler = BackgroundScheduler()
scheduler.add_job(func=sync_users, trigger="interval", seconds=sync_interval_seconds)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

def create_app():
    app = Flask(__name__)
    app.register_blueprint(users_sync_api, url_prefix='/api/syncService/users')
    app.register_blueprint(stats_sync_api, url_prefix='/api/syncService/stats')

    return app

def main():
    app = create_app()
    app.run(host='0.0.0.0', port = 5001)