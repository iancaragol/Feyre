import os

from flask import Flask
from sync_service.api.sync_user import sync_api

def create_app():
    app = Flask(__name__)
    app.register_blueprint(sync_api, url_prefix='/syncService/api/users')

    return app

def main():
    app = create_app()
    app.run(host='0.0.0.0', port = 5001)  