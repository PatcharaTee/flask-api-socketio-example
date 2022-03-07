from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_cors import CORS
from flask import Flask

from datetime import timedelta
import dotenv
import os

# Load .env
dotenv.load_dotenv(os.path.join(os.getcwd(), ".env"))

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
        SECRET_KEY=os.getenv('SECRET_KEY'),
        JWT_SECRET_KEY=os.getenv('JWT_SECRET_KEY'),
        JWT_ACCESS_TOKEN_EXPIRES=timedelta(hours=1),
        SQLALCHEMY_DATABASE_URI=os.getenv('SQLALCHEMY_DATABASE_URI'),
        SQLALCHEMY_ECHO=True,
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )
    
    # Initialize flask extensions
    db.init_app(app)
    cors.init_app(
        app,
        supports_credentials=True,
        resources={r'/*': {'origins': ['http://localhost:4200', 
                                       'https://flask-api-socketio-example-fe.herokuapp.com']}}
    )
    jwt.init_app(app)
    socketio.init_app(
        app,
        async_handlers=True,
        async_mode="eventlet",
        cors_credentials=True,
        cors_allowed_origins=['http://localhost:4200', 
                              'https://flask-api-socketio-example-fe.herokuapp.com'],
        logger=True,
        engineio_logger=True
    )

    app.register_blueprint(auth_api)
    app.register_blueprint(room_api)
    
    return app
