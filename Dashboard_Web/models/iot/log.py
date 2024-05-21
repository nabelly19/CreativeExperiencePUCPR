from models import db
from models.db import datetime

class Log(db.Model):
    __tablename__ = 'log'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    
    information = db.Column(db.String(200))
    creation_date = db.Column(db.DateTime, nullable = False, default=datetime.now)

    # Foreign Key
    topic_id= db.Column(db.Integer, db.ForeignKey('topic.id',  ondelete='SET NULL'), nullable=True)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id', ondelete='SET NULL'), nullable=True)

    # Relationships
    topic = db.relationship('Topic', foreign_keys=[topic_id], back_populates='log', lazy=True, uselist=False)
    device = db.relationship('Device', foreign_keys=[device_id], back_populates='log', lazy=True, uselist=False)
