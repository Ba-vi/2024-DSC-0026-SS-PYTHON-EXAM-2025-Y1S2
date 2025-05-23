from app.extensions import db
from datetime import datetime


class Program(db.Model):

    __tablename__ = 'programs'
    program_id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return f"Program {self.name}"