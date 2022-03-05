from werkzeug.security import (
    check_password_hash,
    generate_password_hash
)
from flask import (
    Blueprint,
    request,
    jsonify
)
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import (
    create_access_token, jwt_required
)
from . import db
from .models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=['POST'])
def register():
    if 'username' not in request.form or 'password' not in request.form:
        return jsonify({'message': 'Bad request.', 'status': 400}), 400

    username = request.form['username']
    password = request.form['password']

    user = User(username, generate_password_hash(password))

    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        return jsonify({'message': f"User {username} already registered.", 'status': 422}), 422

    return jsonify({'message': 'Ok.', 'status': 200}), 200


@bp.route('/login', methods=['POST'])
def login():
    if 'username' not in request.form or 'password' not in request.form:
        return jsonify({'message': 'Bad request.', 'status': 400}), 400

    username = request.form['username']
    password = request.form['password']

    user = User.query.filter_by(username=username).first()

    if user is None:
        return jsonify({'message': 'Incorrect username.', 'status': 422}), 422
    elif not check_password_hash(user.password, password):
        return jsonify({'message': 'Incorrect password.', 'status': 422}), 422

    user_id = user.id

    access_token = create_access_token(user_id)

    return jsonify({'message': 'Ok.', 'id': user_id, 'access_token': access_token, 'status': 200}), 200


@bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    return jsonify({'message': 'Ok.', 'status': 200}), 200
