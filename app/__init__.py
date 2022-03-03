from datetime import timedelta
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask import Flask
import os

from app.db import DB
from . import auth, room


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='e9270d8e788b56b06af20918fffd99ec',
        JWT_SECRET_KEY='4b6e55781c8147123bb3e093d6fe04ed',
        JWT_ACCESS_TOKEN_EXPIRES=timedelta(hours=1),
        DATABASE=os.path.join(app.instance_path, 'app.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    DB(app)
    CORS(app, supports_credentials=True,
         resources={r'/*': {'origins': ['http://127.0.0.1:5000']}})
    JWTManager(app)

    app.register_blueprint(auth.bp)
    app.register_blueprint(room.bp)

    return app
