from flask import Flask
from backend_service.api.controller.roll_controller import roll_api
from backend_service.api.controller.stats_controller import stats_api

def create_app():
    app = Flask(__name__)
    app.register_blueprint(roll_api, url_prefix='/backendService/api/roll')
    app.register_blueprint(stats_api, url_prefix='/backendService/api/stats')

    return app

def main():
    app = create_app()
    app.run(host='0.0.0.0', port = 5000)  