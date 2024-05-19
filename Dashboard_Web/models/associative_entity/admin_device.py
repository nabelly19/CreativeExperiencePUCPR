from models import db
from models.db import datetime

class AdminDevice(db.Model):
    __tablename__ = 'admin_device'

    # Primary key Foreign keys - PK FK
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), primary_key=True, nullable=False)

    # Foreign keys
    device_id = db.Column(db.Integer, db.ForeignKey('device.id', ondelete='SET NULL'), nullable=True)
    update_admin_id = db.Column(db.Integer, nullable=False) # Para auditoria
    
    # Atributos
    update_date = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    # Relationship
    admin = db.relationship('Admin', back_populates='admin_device', lazy=True)
    device = db.relationship('Device', back_populates='admin_device', lazy=True)
    