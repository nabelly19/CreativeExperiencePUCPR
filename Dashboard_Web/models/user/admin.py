from models import db
from models.db import datetime
from models.validate.integrity import create_with_integrity, update_with_integrity


class Admin(db.Model):
    __tablename__ = 'admin'

    id= db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    
    creation_date = db.Column(db.DateTime, nullable = False)
    update_date = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    # Foreign Key
    role_id= db.Column(db.Integer, db.ForeignKey('role.id', ondelete='SET NULL'), nullable=True)

    # Relationships
    user = db.relationship('Users', back_populates='admin', lazy=True)
    role = db.relationship('Role', back_populates='admin', lazy=True, uselist=False)
    admin_device = db.relationship('AdminDevice', back_populates='admin', cascade='all, delete', lazy=True)

#function to create a new admin
def create_admin(user_id, role_id):
    new_admin = Admin(
        id=user_id,
        role_id=role_id,
        creation_date = datetime.now()
    )
    return create_with_integrity(new_admin, Admin.__tablename__)

#method to find a certain admin
def get_single_admin(user_id):
    admin = Admin.query.filter(Admin.id == user_id).first()
    return admin

#function to get all admins listed
def get_all_admins():
    all_admins = Admin.query.all()
    return all_admins

#function to update an admin
def update_admin(user_id, new_role_id=None, new_creation_date=None):
    admin = get_single_admin(user_id)
    
    if admin is not None:
        if new_role_id is not None:
            admin.role_id = new_role_id
        if new_creation_date is not None:
            admin.creation_date = new_creation_date
            admin.update_date = datetime.now()
    
    return update_with_integrity(admin, Admin.__tablename__)

