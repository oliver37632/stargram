from flask import Flask
from flask_jwt_extended import JWTManager
from src.router import bp


def create_app():
    _app = Flask(__name__)

    jwt = JWTManager(_app)

    _app.register_blueprint(bp)
    return _app