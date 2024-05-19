from models import db
from models.iot.device import Device
from models.user.admin import Admin
from models.db import datetime

class AdminDevice(db.Model):
    __tablename__ = 'admin_device'

    # Primary key Foreign keys - PK FK
    admin_id = db.Column(db.Integer, db.ForeignKey(Admin.id), primary_key=True, nullable=False)

    # Foreign keys
    update_admin_id = db.Column(db.Integer, db.ForeignKey(Admin.id), nullable=False) # Para auditoria
    device_id = db.Column(db.Integer, db.ForeignKey(Device.id, ondelete='SET NULL'), nullable=True)
    
    # Atributos
    update_date = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    # Relationship
    admin = db.relationship('Admin', foreign_keys=[admin_id], back_populates='admin_device', lazy=True)
    update_admin = db.relationship('Admin', foreign_keys=[update_admin_id], back_populates='admin_device', lazy=True)
    device = db.relationship('Device', foreign_keys=[device_id], back_populates='admin_device', lazy=True)
