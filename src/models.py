from . import db


class User(db.Model):

    """The User model."""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password


class Room(db.Model):

    """The Room model."""
    __tablename__ = 'rooms'
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(50), nullable=False, unique=True)
    locked = db.Column(db.Boolean, nullable=False, default=False)
    password = db.Column(db.String(256), nullable=False)

    def __init__(self, owner_id, name, locked, password):
        self.owner_id = owner_id
        self.name = name
        self.locked = locked
        self.password = password

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'owner_id': self.owner_id,
            'name': self.name,
            'locked': self.locked,
        }
