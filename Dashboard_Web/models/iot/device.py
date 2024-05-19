from models.db import db
from models.iot.log import Log
from models.associative_entity.admin_device import AdminDevice
from models.db import datetime
from enum import Enum

# Definição de Enum para o tipo de dispositivo
class DeviceType(Enum):
    SENSOR = 'Sensor'
    ATUADOR = 'Atuador'

class Device(db.Model):
    __tablename__ = 'device'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    name = db.Column(db.String(100), nullable=False)
    brand = db.Column(db.String(100), nullable=False)
    type = db.Column(db.Enum(DeviceType), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=False)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.now)

    # Relationship
    admin_device = db.relationship('AdminDevice', foreign_keys=[AdminDevice.device_id], back_populates='device', cascade='all, delete', lazy=True)
    log = db.relationship('Log', foreign_keys=[Log.id], back_populates='device', cascade='all, delete', lazy=True)
