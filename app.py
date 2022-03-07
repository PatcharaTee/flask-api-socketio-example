import eventlet
eventlet.monkey_patch()

from src import create_app, db, socketio

app = create_app()

with app.app_context():
    print('Test DB connection...')
    table_list = db.get_tables_for_bind()
    if table_list != None:
        print('DB is connected.')
    # db.drop_all()
    # db.create_all()

if __name__ == '__main__':
    socketio.run(app)
