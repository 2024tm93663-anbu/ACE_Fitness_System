from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    age = db.Column(db.Integer)
    height = db.Column(db.Float)
    weight = db.Column(db.Float)
    program = db.Column(db.String(50))
    calories = db.Column(db.Integer)
    target_weight = db.Column(db.Float)
    target_adherence = db.Column(db.Integer)

class Progress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(100), db.ForeignKey('client.name'), nullable=False)
    week = db.Column(db.String(20))
    adherence = db.Column(db.Integer)

class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(100), db.ForeignKey('client.name'), nullable=False)
    date = db.Column(db.String(10))
    workout_type = db.Column(db.String(50))
    duration_min = db.Column(db.Integer)
    notes = db.Column(db.Text)
    exercises = db.relationship('Exercise', backref='workout', lazy=True, cascade="all, delete-orphan")

class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workout.id'), nullable=False)
    name = db.Column(db.String(100))
    sets = db.Column(db.Integer)
    reps = db.Column(db.Integer)
    weight = db.Column(db.Float)

class Metric(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(100), db.ForeignKey('client.name'), nullable=False)
    date = db.Column(db.String(10))
    weight = db.Column(db.Float)
    waist = db.Column(db.Float)
    bodyfat = db.Column(db.Float)
