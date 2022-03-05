from flask import (
    Blueprint,
    request,
    jsonify
)
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)
from . import db
from .models import Room

bp = Blueprint('room', __name__, url_prefix='/room')


@bp.route('/create', methods=['POST'])
@jwt_required()
def create():
    if not request.is_json:
        return jsonify({'message': 'Bad request.', 'status': 400})

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

    try:
        room = Room(owner_id, name, locked, password)
        db.session.add(room)
        db.session.commit()
    except IntegrityError:
        return jsonify({'message': 'this room already exist.', 'status': 200})

    return jsonify({'message': 'Ok.', 'status': 200})


@bp.route('/list', methods=['GET'])
@jwt_required()
def list():

    rooms = Room.query.all()
    rooms = [room.serialize for room in rooms]

    return jsonify({'rooms': rooms, 'status': 200}), 200


@bp.route('/close', methods=['DELETE'])
@jwt_required()
def close():

    room_id = request.args.get('room_id', '')
    owner_id = get_jwt_identity()

    if room_id == '' or owner_id == '':
        return jsonify({'message': 'Bad request.', 'status': 400}), 400

    room = Room.query.filter_by(id=room_id).first()

    if room is None:
        return jsonify({'message': 'Bad request.', 'status': 400}), 400

    if owner_id == room['owner_id']:
        db.session.delete(room)
        db.session.commit()
    else:
        return jsonify({'message': 'Access denied.', 'status': 401}), 401

    return jsonify({'message': 'Ok.', 'status': 200}), 200
