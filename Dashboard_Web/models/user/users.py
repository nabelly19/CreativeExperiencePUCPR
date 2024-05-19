from models.db import db
from models.user.contact import Contact
from models.user.admin import Admin
from models.user.client import Client
from models.db import datetime

class Users(db.Model):
    __tablename__ = 'users'

    id= db.Column(db.Integer, autoincrement=True, primary_key=True)
    
    name= db.Column(db.String(100), nullable= False)
    cpf= db.Column(db.String(11), nullable= False, unique=True)
    birth_date = db.Column(db.Date(), nullable = False)
    gender= db.Column(db.String(50), nullable= False)
    email= db.Column(db.String(11), nullable= False, unique=True)
    is_active= db.Column(db.Boolean, nullable= False, default= False)
    
    creation_date = db.Column(db.DateTime, nullable = False, default=datetime.now)
    update_date = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    # Relationship (bidirecional)
    contact = db.relationship('Contact', foreign_keys=[Contact.id], back_populates='users', cascade='all, delete-orphan', lazy=True)
    admin = db.relationship('Admin', foreign_keys=[Admin.id], back_populates='users',  cascade='all, delete-orphan', lazy=True, uselist=False)
    client = db.relationship('Client', foreign_keys=[Client.id], back_populates='users', cascade='all, delete-orphan', lazy=True, uselist=False)
