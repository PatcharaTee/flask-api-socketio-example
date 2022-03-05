from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_cors import CORS
from flask import Flask

from datetime import timedelta
import os

# Flask extensions
cors = CORS()
db = SQLAlchemy()
jwt = JWTManager()
socketio = SocketIO()

# Import DB models so that they are registered with SQLAlchemy
from . import models as _

# Import Socket.IO events so that they are registered with Flask-SocketIO
from . import events as _

from .auth import bp as auth_api
from .room import bp as room_api


def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='e9270d8e788b56b06af20918fffd99ec',
        JWT_SECRET_KEY='4b6e55781c8147123bb3e093d6fe04ed',
        JWT_ACCESS_TOKEN_EXPIRES=timedelta(hours=1),
        SQLALCHEMY_DATABASE_URI="postgresql://tijswukmrpxjhg:02f1a8e92041b515ab89ca6dc992a5435a02bd42ba2943e8872c0a94a827d91d@ec2-34-231-183-74.compute-1.amazonaws.com:5432/dfntls9ij79eqs",
        SQLALCHEMY_ECHO=True,
        SQLALCHEMY_TRACK_MODIFICATIONS=False
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
        resources={r'/*': {'origins': ['http://localhost:4200', 'https://flask-api-socketio-example-fe.herokuapp.com']}}
    )
    jwt.init_app(app)
    socketio.init_app(
        app,
        async_handlers=True,
        async_mode="eventlet",
        cors_credentials=True,
        cors_allowed_origins=['http://localhost:4200', 'https://flask-api-socketio-example-fe.herokuapp.com'],
        logger=True,
        engineio_logger=True
    )

    app.register_blueprint(auth_api)
    app.register_blueprint(room_api)
    
    return app
