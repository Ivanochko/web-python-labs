from .. import db


class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False, unique=True)


class Worker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    mobile = db.Column(db.String(50), nullable=False)
    salary = db.Column(db.Integer(), nullable=False)
    hired_at = db.Column(db.DateTime, default=db.func.now())
    grade_id = db.Column(db.Integer, db.ForeignKey('grade.id'), nullable=False)


db.create_all()
