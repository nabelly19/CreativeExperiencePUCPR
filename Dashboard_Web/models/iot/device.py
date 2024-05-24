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
    creation_date = db.Column(db.DateTime, nullable=False)

    # Relationship
    admin_device = db.relationship('AdminDevice', back_populates='device', cascade='all, delete', lazy=True)
    log = db.relationship('Log', back_populates='device', cascade='all, delete', lazy=True)
    topic = db.relationship('Topic', back_populates='device', cascade='all, delete', lazy=True)


    def create_device(name, brand, type, is_active):
        new_device = Device(name = name, 
                        brand = brand, 
                        type = type, 
                        is_active = is_active,
                        creation_date = datetime.now())
        
        return create_with_integrity(new_device, Device.__tablename__)
    
    def get_single_device(id):
        device = Device.query.get(id)
        if device is not None:
            return device    
    
    def get_devices_with_topics():
        devices = Device.query.options(joinedload(Device.topic)).all()
        return devices
    
    def delete_device(device_id):
        device = Device.query.get(device_id)
        if device:
            db.session.delete(device)
            db.session.commit()
        return Device.get_devices_with_topics()

    def update_device(name, brand, type, is_active, device_id):
        device = Device.get_single_device(device_id)
        
        if device is not None:
            device.name = name
            device.brand = brand
            device.type = type
            device.is_active = is_active
            
            return update_with_integrity(device, Device.__tablename__)
