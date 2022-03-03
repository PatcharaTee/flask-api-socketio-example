from . import db, socketio


@socketio.on('connect')
def on_connect():
    print("User connect.")


@socketio.on('disconnect')
def on_disconnect():
    print("User disconnect.")
