from models import db
from models.db import datetime
from models.validate.integrity import *

class Topic(db.Model):
    __tablename__ = 'topic'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    title = db.Column(db.String(100), nullable=False)
    creation_date = db.Column(db.DateTime, nullable = False, default=datetime.now)
    update_date = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    # Foreign keys
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=False)

    # Relationship
    log = db.relationship('Log', back_populates='topic', cascade='all, delete', lazy=True)
    device = db.relationship('Device', back_populates='topic', lazy=True)

    def create_topic(title, device_id):
        new_topic = Topic(title = title, device_id = device_id)

        return create_with_integrity(new_topic, Topic.__tablename__)
    