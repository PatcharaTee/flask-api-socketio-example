from werkzeug.security import (
    check_password_hash,
    generate_password_hash
)
from flask import (
    Blueprint,
    g, request, session,
    jsonify
)
from flask_jwt_extended import (
    create_access_token, jwt_required
)
from src.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=['POST'])
def register():
    if 'username' not in request.form or 'password' not in request.form:
        return jsonify({'message': 'Bad request.', 'status': 400})

    username = request.form['username']
    password = request.form['password']
    
    db = get_db()

    try:
        db.execute(
            "INSERT INTO user (username, password) VALUES (?, ?)",
            (username, generate_password_hash(password))
        )
        db.commit()
    except db.IntegrityError:
        return jsonify({'message': f"User {username} already registered.", 'status': 200})

    return jsonify({'message': 'Ok.', 'status': 200})


@bp.route('/login', methods=['POST'])
def login():
    if 'username' not in request.form or 'password' not in request.form:
        return jsonify({'message': 'Bad request.', 'status': 400})

    username = request.form['username']
    password = request.form['password']
    
    db = get_db()

    user = db.execute(
        "SELECT * FROM user WHERE username = ?",
        (username,)
    ).fetchone()

    if user is None:
        return jsonify({'message': 'Incorrect username.', 'status': 200})
    elif not check_password_hash(user['password'], password):
        return jsonify({'message': 'Incorrect password.', 'status': 200})

    user_id = user['id']

    session.clear()
    session['user_id'] = user_id

    access_token = create_access_token(user['id'])

    return jsonify({'message': 'Ok.', 'id': user_id, 'access_token': access_token, 'status': 200})


@bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    session.clear()
    return jsonify({'message': 'Ok.', 'status': 200})


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        db = get_db()
        g.user = db.execute(
            "SELECT * FROM user WHERE id = ?",
            (user_id,)
        )
