from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin


db = SQLAlchemy()

class User(db.Model,SerializerMixin):
    __tablename__='users'
    serialize_rules = ('-houses.user',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String,nullable=False, unique=True)

    houses = db.relationship('House',backref='user')

    def __repr__(self):
        return f'<The current user id {self.name}>'

    
    

class House(db.Model,SerializerMixin):
    __tablename__='houses'
    serialize_rules = ('-user.houses',)

    id = db.Column(db.Integer, primary_key=True)
    no = db.Column(db.Integer, unique=True)
    location = db.Column(db.String)

    user_id= db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f'<The house number is {self.no}>'

    