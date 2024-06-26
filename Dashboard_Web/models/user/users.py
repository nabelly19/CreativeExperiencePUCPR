from flask_login import UserMixin
from models.db import db, datetime
from sqlalchemy.orm import joinedload
from models.validate.integrity import create_with_integrity, update_with_integrity, delete_with_integrity
from models.user.admin import Admin 
from models.user.role import Role


#Users class, atributes and methods. The "db" from our models.py is being imported in order to create the data base especifications
class Users(UserMixin, db.Model):
    __tablename__ = 'users'

    id= db.Column(db.Integer, autoincrement=True, primary_key=True)
    
    name= db.Column(db.String(255), nullable= False)
    cpf= db.Column(db.String(11), nullable= False, unique=True)
    birth_date = db.Column(db.Date, nullable = False)
    email = db.Column(db.String(50), nullable= False, unique=True)
    nickname= db.Column(db.String(50), nullable= False, unique=True)
    password = db.Column(db.String(200), nullable= False)
    is_active= db.Column(db.Boolean, nullable=False, default=True)
    
    creation_date = db.Column(db.DateTime, nullable=False)
    update_date = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    # Relationship (bidirecional)
    admin = db.relationship('Admin', back_populates='user',  cascade='all, delete-orphan', uselist=False, lazy=True)
    client = db.relationship('Client', back_populates='user', cascade='all, delete-orphan', uselist=False, lazy=True)

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

    def check_role(self, target_role):
        user_id = self.id
        admin = Admin.query.filter_by(id=user_id).first()
        role_id = admin.role_id
        role = Role.query.filter_by(id=role_id).first()

        return role.name == target_role

    def is_operator(self):
        try:
            return Users.check_role(self, "Operador")
        except:
            return False
        
    def is_statistical(self):
        try:
            return Users.check_role(self, "Estatístico")
        except:
            return False   
         
    def is_root(self):
        try:
            return Users.check_role(self, "Root")
        except:
            return False
         
    def get_single_user(nickname):
        user = Users.query.filter_by(nickname=nickname).first()
        if user is not None : return user

    def get_single_user_id(user_id):
        user = Users.query.get(user_id)
        if user is not None : return user

    def create_user(name, cpf, birth_date, email, nickname, password):
        new_user = Users(
            name = name,
            cpf = cpf,
            birth_date = birth_date,
            email = email,
            nickname = nickname,
            password = password,
            creation_date = datetime.now()
        )
        
        return create_with_integrity(new_user, Users.__tablename__)
    
        #method to update the user's information
    def update_user(id, name, email, nickname, is_active, cpf, birth_date):
        user = Users.get_single_user_id(id)

        if user is not None:
            user.name = name
            user.email = email
            user.nickname = nickname
            user.is_active = is_active
            user.cpf = cpf
            user.birth_date = birth_date
            #user.password = password

        return update_with_integrity(user, Users.__tablename__)

    def delete_user(user_id):
        user = Users.query.get(user_id)
        
        delete_with_integrity(user, Users.__tablename__)
        return user_id

    def get_users_with_admin_client():
        users = Users.query.options(joinedload(Users.admin), joinedload(Users.client)).all()
        return users