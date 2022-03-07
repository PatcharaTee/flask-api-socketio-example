from sqlalchemy.exc import IntegrityError
from werkzeug.security import (
    check_password_hash,
    generate_password_hash
)
from flask import (
    Blueprint,
    request,
    jsonify
)
from flask_jwt_extended import (
    create_access_token, jwt_required,
    get_jwt_identity, get_jwt
)
from . import db, jwt
from .models import TokenBlocklist, User

from datetime import datetime
from datetime import timezone

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
    jti = get_jwt()["jti"]
    user_id = get_jwt_identity()
    now = datetime.now(timezone.utc)

    blocked_token = TokenBlocklist(user_id, jti, now)

    db.session.add(blocked_token)
    db.session.commit()

    return jsonify({'message': 'Ok.', 'status': 200}), 200


@bp.route('/verify_token', methods=['GET'])
@jwt_required()
def verify():
    return jsonify({'message': 'Ok.', 'status': 200}), 200


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()

    return token is not None
