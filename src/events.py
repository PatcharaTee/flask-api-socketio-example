from flask_socketio import emit, join_room, leave_room
from flask import request
from . import socketio

from datetime import datetime
import pytz


@socketio.on('connect')
def handle_connect():
    sid = request.sid
    print(sid, "connect")


@socketio.on('disconnect')
def handle_connect():
    sid = request.sid
    print(sid, "disconnect")


@socketio.on('join_room')
def handle_join_room(json):
    sid = request.sid
    room_id = json['room_id']
    username = json['username']

    join_room(room_id, sid)
    emit('room', {'msg': f'User {username} join room'},
         broadcast=True, include_self=False, room=room_id)


@socketio.on('leave_room')
def handle_leave_room(json):
    sid = request.sid
    room_id = json['room_id']
    username = json['username']

    leave_room(room_id, sid)
    emit('room', {'msg': f'User {username} leave room'},
         broadcast=True, include_self=False, room=room_id)


@socketio.on('send_message')
def handle_send_message(json):
    sid = request.sid
    room_id = json['room_id']
    message = json['message']

    print('User', sid, 'send message to room', room_id, '.')

    timestamp = datetime.now(pytz.timezone('Asia/Bangkok')).timestamp()

    emit('new_msg', {'msg': message, 'timestamp': timestamp},
         broadcast=True, room=room_id)
