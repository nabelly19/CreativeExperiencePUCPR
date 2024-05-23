from flask_login import UserMixin
from models.db import db, datetime
from models.validate.integrity import *

class Users(UserMixin, db.Model):
    __tablename__ = 'users'

    id= db.Column(db.Integer, autoincrement=True, primary_key=True)
    
    name= db.Column(db.String(255), nullable= False)
    cpf= db.Column(db.String(11), nullable= False, unique=True)
    birth_date = db.Column(db.Date, nullable = False)
    gender= db.Column(db.String(50), nullable= False)
    email= db.Column(db.String(50), nullable= False, unique=True)
    nickname= db.Column(db.String(20), nullable= False, unique=True)
    password = db.Column(db.String(200), nullable= False)
    is_active= db.Column(db.Boolean, nullable=False, default=True)
    
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
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
    
    def get_single_user(nickname):
        user = Users.query.filter_by(nickname=nickname).first()
        if user is not None : return user

    def create_user(name, cpf, birth_date, gender, email, nickname, password):
        new_user = Users(
            name = name,
            cpf = cpf,
            birth_date = birth_date,
            gender = gender,
            email = email,
            nickname = nickname,
            password = password,
        )
        
        return create_with_integrity(new_user, Users.__tablename__)
