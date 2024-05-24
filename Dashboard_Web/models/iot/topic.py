from models import db
from models.db import datetime
from models.validate.integrity import *

class Topic(db.Model):
    __tablename__ = 'topic'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    title = db.Column(db.String(100), nullable=False)
    creation_date = db.Column(db.DateTime, nullable = False)
    update_date = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    # Foreign keys
    device_id = db.Column(db.Integer, db.ForeignKey('device.id', ondelete='SET NULL'), nullable=True)

    # Relationship
    log = db.relationship('Log', back_populates='topic', cascade='all, delete', lazy=True)
    device = db.relationship('Device', back_populates='topic', lazy=True)

    def create_topic(title, device_id):
        new_topic = Topic(title = title,
                          creation_date = datetime.now(), 
                          device_id = device_id)
        return create_with_integrity(new_topic, Topic.__tablename__)
    
    def get_single_topic(name):
        topic = Topic.query.filter(Topic.title == name).first()
        if topic is not None:
            return topic

    def update_topic(new_title, old_title):
        topic = Topic.get_single_topic(old_title)
        
        if topic is not None:
            topic.title = new_title

            return update_with_integrity(topic, Topic.__tablename__)
