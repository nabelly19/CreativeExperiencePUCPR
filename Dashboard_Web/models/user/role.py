from models import db
from models.db import datetime
from models.validate.integrity import create_with_integrity, update_with_integrity

#Role class, atributes and methods. The "db" from our models.py is being imported in order to create the data base especifications
class Role(db.Model):
    __tablename__ = 'role'

    id= db.Column(db.Integer, autoincrement=True, primary_key=True)
    
    name= db.Column(db.String(50), nullable= False, unique=True)
    creation_date = db.Column(db.DateTime, nullable = False, default=datetime.now)

    # Relationship
    admin = db.relationship('Admin', back_populates='role', lazy=True)

    def create_role(name):
        new_role = Role(
            name=name,
            creation_date=datetime.now()
        )
        return create_with_integrity(new_role, Role.__tablename__)

    def get_single_role(role_id):
        role = Role.query.filter(Role.id == role_id).first()
        return role

    def get_all_roles():
        all_roles = Role.query.all()
        return all_roles

    def update_role(role_id, new_name=None):
        role = Role.get_single_role(role_id)

        if role is not None:
            if new_name is not None:
                role.name = new_name

        return update_with_integrity(role, Role.__tablename__)

