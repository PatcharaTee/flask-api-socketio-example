import eventlet
eventlet.monkey_patch()

from src import create_app, db, socketio

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

if __name__ == '__main__':
    socketio.run(app)
