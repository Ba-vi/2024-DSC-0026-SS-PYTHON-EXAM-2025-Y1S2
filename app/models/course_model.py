from app.extensions import db, migrate
from datetime import datetime



class Course(db.Model):

    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now)
    program_id = db.Column(db.Integer, db.ForeignKey('programs.program_id'), nullable=False)


    def __init__(self, name, program_id):
        self.name = name
        self.program_id = program_id

    def __repr__(self):
        return f"Course {self.name}"
    