from models import db
from models.db import datetime

class Admin(db.Model):
    __tablename__ = 'admin'

    id= db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    
    creation_date = db.Column(db.DateTime, nullable = False, default=datetime.now)
    update_date = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    # Foreign Key
    role_id= db.Column(db.Integer, db.ForeignKey('role.id', ondelete='SET NULL'), nullable=True)

    # Relationships
    user = db.relationship('Users', back_populates='admin', lazy=True)
    role = db.relationship('Role', back_populates='admin', lazy=True, uselist=False)
    admin_device = db.relationship('AdminDevice', back_populates='admin', cascade='all, delete', lazy=True)
