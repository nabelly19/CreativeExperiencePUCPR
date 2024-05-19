from models import db
from models.db import datetime

class Topic(db.Model):
    __tablename__ = 'topic'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    
    creation_date = db.Column(db.DateTime, nullable = False, default=datetime.now)
    update_date = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    information = db.Column(db.String(200))

    # Relationship
    log = db.relationship('Log', back_populates='topic', cascade='all, delete', lazy=True)
