from sqlalchemy import Column, ForeignKey, Integer, String
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Planet(db.Model):
    __tablename__ = 'planet'
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(250), nullable=False)
    climate = db.Column(String(250), nullable=False)
    population = db.Column(Integer, nullable=False)
    orbital_period = db.Column(Integer, nullable=False)
    diameter = db.Column(Integer, nullable=False)

    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            # do not serialize the password, its a security breach
        }

class Character(db.Model):
    __tablename__ = 'character'
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(250), nullable=False)
    birth_year = db.Column(String(250), nullable=False)
    height = db.Column(Integer, nullable=False)
    skin_color = db.Column(String(100), nullable=False)
    eye_color = db.Column(String(100), nullable=False)

    def __repr__(self):
        return '<Character %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            # do not serialize the password, its a security breach
        }