from models.db import db, datetime
from models.iot.topic import Topic
from models.validate.integrity import *
from sqlalchemy.orm import joinedload
from enum import Enum

# Definição de Enum para o tipo de dispositivo
class DeviceType(Enum):
    Sensor = 'Sensor'
    Atuador = 'Atuador'

class Device(db.Model):
    __tablename__ = 'device'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    name = db.Column(db.String(100), nullable=False)
    brand = db.Column(db.String(100), nullable=False)
    type = db.Column(db.Enum(DeviceType), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=False)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.now)

    # Relationship
    admin_device = db.relationship('AdminDevice', back_populates='device', cascade='all, delete', lazy=True)
    log = db.relationship('Log', back_populates='device', cascade='all, delete', lazy=True)
    topic = db.relationship('Topic', back_populates='device', lazy='joined')


    def create_device(name, brand, type, is_active):
        new_device = Device(name = name, 
                        brand = brand, 
                        type = type, 
                        is_active = is_active)
        
        return create_with_integrity(new_device, Device.__tablename__)
    
    def get_sensors_with_topics():
        devices = Device.query.options(joinedload(Device.topic)).all()
        return devices
