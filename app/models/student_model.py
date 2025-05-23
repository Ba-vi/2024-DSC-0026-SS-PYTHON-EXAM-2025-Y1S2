from app.extensions import db
from datetime import datetime



class Student(db.Model):

    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    contact = db.Column(db.String(15), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    program_id = db.Column(db.Integer, db.ForeignKey('programs.program_id'), nullable=False)

    def __init__(self, name, email, program_id, contact):
        self.contact = contact
        self.name = name
        self.email = email
        self.program_id = program_id

    def __repr__(self):
        return f"Student {self.name}"

