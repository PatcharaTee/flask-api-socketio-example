from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO
from flask_cors import CORS
from flask import Flask
from src.db import DB

from datetime import timedelta
import os

from .auth import bp as auth_api
from .room import bp as room_api

# Flask extensions
db = DB()
cors = CORS()
jwt = JWTManager()
socketio = SocketIO()

# Import Socket.IO events so that they are registered with Flask-SocketIO
from . import events as _

def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='e9270d8e788b56b06af20918fffd99ec',
        JWT_SECRET_KEY='4b6e55781c8147123bb3e093d6fe04ed',
        JWT_ACCESS_TOKEN_EXPIRES=timedelta(hours=1),
        DATABASE=os.path.join(app.instance_path, 'app.sqlite'),
    )

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # Initialize flask extensions
    db.init_app(app)
    cors.init_app(
        app,
        supports_credentials=True,
        resources={r'/*': {'origins': '*'}}
    )
    jwt.init_app(app)
    socketio.init_app(
        app,
        async_handlers=True,
        async_mode="eventlet",
        cors_credentials=True,
        cors_allowed_origins='*',
        logger=True,
        engineio_logger=True
    )

    app.register_blueprint(auth_api)
    app.register_blueprint(room_api)
    
    return app
