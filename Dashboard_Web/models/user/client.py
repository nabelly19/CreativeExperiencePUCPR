from models import db
from models.db import datetime

class Client(db.Model):
    __tablename__ = 'client'

    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    update_date = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    # Relationship
    user = db.relationship('Users', back_populates='client', lazy=True)
