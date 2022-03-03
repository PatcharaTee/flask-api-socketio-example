from flask import (
    Blueprint,
    request,
    jsonify
)
from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)
from app.db import get_db

bp = Blueprint('room', __name__, url_prefix='/room')


@bp.route('/create', methods=['POST'])
@jwt_required()
def create():
    if not request.is_json:
        return jsonify({'message': 'Bad request.', 'status': 400})

    db = get_db()

    json_body = request.get_json()

    if 'name' in json_body:
        name = json_body['name']
    else:
        return jsonify({'message': 'Bad request.', 'status': 400})

    if 'locked' in json_body:
        locked = json_body['locked']
        if locked:
            if 'password' in json_body and json_body['password'] != '':
                password = json_body['password']
            else:
                return jsonify({'message': 'Bad request.', 'status': 400})
        else:
            locked = False
            password = ""

    owner_id = get_jwt_identity()
    user = db.execute(
        "SELECT * FROM user WHERE id = ?",
        (owner_id,)
    ).fetchone()

    user_id = user['id']

    try:
        db.execute(
            "INSERT INTO room (owner_id, name, locked, password) VALUES (?, ?, ?, ?)",
            (user_id, name, locked, password)
        )
        db.commit()
    except db.IntegrityError:
        return jsonify({'message': 'this room already exist.', 'status': 200})

    return jsonify({'message': 'Ok.', 'status': 200})


@bp.route('/list', methods=['GET'])
@jwt_required()
def list():
    db = get_db()

    rooms = db.execute(
        "SELECT id, name, locked, owner_id FROM room"
    ).fetchall()
    rooms = [dict(i) for i in rooms]

    return jsonify({'rooms': rooms, 'status': 200})


@bp.route('/close', methods=['DELETE'])
@jwt_required()
def close():
    if not request.is_json:
        return jsonify({'message': 'Bad request.', 'status': 400})

    db = get_db()

    json_body = request.get_json()

    if 'room_id' in json_body and 'owner_id' in json_body:
        room_id = json_body['room_id']
        owner_id = json_body['owner_id']
    else:
        return jsonify({'message': 'Bad request.', 'status': 400})

    room = db.execute(
        "SELECT * FROM room WHERE id = ?",
        (room_id,)
    ).fetchone()

    if room is None:
        return jsonify({'message': 'Bad request.', 'status': 400})

    if owner_id == room['owner_id']:
        db.execute(
            "DELETE FROM room WHERE id = ?",
            (room_id,)
        )
        db.commit()
    else:
        return jsonify({'message': 'Access denied.', 'status': 401})

    return jsonify({'message': 'Ok.', 'status': 200})
