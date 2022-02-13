import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_user import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class Material(db.Model):
    __tablename__ = 'materials'
    id = db.Column(db.Integer, db.Sequence('material_seq'), primary_key=True)
    excel_id = db.Column(db.Integer)
    date_added = db.Column(db.DateTime, default=datetime.datetime.now())
    name = db.Column(db.String(100))
    iron_amount = db.Column(db.Float)
    silicon_amount = db.Column(db.Float)
    aluminum_amount = db.Column(db.Float)
    sodium_amount = db.Column(db.Float)
    sulfur_amount = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("User", backref='users')

    @property
    def serialized(self):
        return {
            'id': self.id,
            '$id': self.excel_id,
            'date_added': self.date_added,
            'name': self.name,
            'iron_amount': self.iron_amount,
            'silicon_amount': self.silicon_amount,
            'aluminum_amount': self.aluminum_amount,
            'sodium_amount': self.sodium_amount,
            'sulfur_amount': self.sulfur_amount,
            'user_id': self.user_id,
            'user': self.user,
        }

    def __repr__(self):
        return f"Material {self.name}"


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, db.Sequence('user_seq'), primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean())
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)

    @property
    def serialized(self):
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'password': self.password,
            'active': self.active,
            'first_name': self.first_name,
            'last_name': self.last_name,
        }

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"User {self.username}"
