from database import db

class Client(db.Model):

    __tablename__ = "clients"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))
    age = db.Column(db.Integer)

    height = db.Column(db.Float)
    weight = db.Column(db.Float)

    program = db.Column(db.String(50))

    calories = db.Column(db.Integer)

    target_adherence = db.Column(db.Integer)