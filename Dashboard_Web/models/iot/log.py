from models import db
from models.iot.topic import Topic
from models.iot.device import Device
from models.db import datetime

class Log(db.Model):
    __tablename__ = 'log'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    
    creation_date = db.Column(db.DateTime, nullable = False, default=datetime.now)

    # Foreign Key
    topic_id= db.Column(db.Integer, db.ForeignKey(Topic.id,  ondelete='SET NULL'), nullable=False)
    device_id = db.Column(db.Integer, db.ForeignKey(Device.id, ondelete='SET NULL'), nullable=False)

    # Relationships
    topic = db.relationship('Topic', foreign_keys=[topic_id], back_populates='log', lazy=True, uselist=False)
    device = db.relationship('Device', foreign_keys=[device_id], back_populates='log', lazy=True, uselist=False)
