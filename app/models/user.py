from app import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), unique=True, nullable=False)
    pwd = db.Column(db.String(128), nullable=False)

    def __init__(self, username, pwd):
        self.username = username
        self.pwd = pwd

    def __repr__(self):
        return {'id': self.id, 'username': self.username}

