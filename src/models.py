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

    @property
    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password
        }


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
        return {
            'id': self.id,
            'owner_id': self.owner_id,
            'name': self.name,
            'locked': self.locked
        }


class TokenBlocklist(db.Model):

    """The TokenBlocklist model."""
    __tablename__ = 'token_block_list'
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, nullable=False)
    jti = db.Column(db.String(36), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, owner_id, jti, created_at):
        self.owner_id = owner_id
        self.jti = jti
        self.created_at = created_at
