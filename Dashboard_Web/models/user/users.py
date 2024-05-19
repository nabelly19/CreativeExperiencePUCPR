from flask_login import UserMixin
from models.db import db
from models.db import datetime

class Users(UserMixin, db.Model):
    __tablename__ = 'users'

    id= db.Column(db.Integer, autoincrement=True, primary_key=True)
    
    name= db.Column(db.String(255), nullable= False)
    cpf= db.Column(db.String(11), nullable= False, unique=True)
    birth_date = db.Column(db.Date, nullable = False)
    gender= db.Column(db.String(50), nullable= False)
    email= db.Column(db.String(50), nullable= False, unique=True)
    nickname= db.Column(db.String(20), nullable= False, unique=True)
    password = db.Column(db.String(100), nullable= False)
    #is_active= db.Column(db.Boolean, nullable= False, default= False)
    
    creation_date = db.Column(db.DateTime, nullable = False, default=datetime.now)
    update_date = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    # Relationship (bidirecional)
    admin = db.relationship('Admin', back_populates='user',  cascade='all, delete-orphan', uselist=False, lazy=True)
    client = db.relationship('Client', back_populates='user', cascade='all, delete-orphan', uselist=False, lazy=True)
    contact = db.relationship('Contact', back_populates='user', cascade='all, delete-orphan', lazy=True)

    def exists_admin(self):
        if self.admin:
            return True
        else:
            return False

    def exists_client(self):
        if self.client:
            return True
        else:
            return False
              