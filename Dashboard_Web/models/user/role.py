from models import db
from models.db import datetime

class Role(db.Model):
    __tablename__ = 'role'

    id= db.Column(db.Integer, autoincrement=True, primary_key=True)
    
    name= db.Column(db.String(50), nullable= False, unique=True)
    creation_date = db.Column(db.DateTime, nullable = False, default=datetime.now)

    # Relationship
    admin = db.relationship('Admin', back_populates='role', lazy=True)
