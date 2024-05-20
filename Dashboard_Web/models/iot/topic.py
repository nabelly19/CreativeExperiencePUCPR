from models import db
from models.db import datetime
from models.validate.integrity import *

class Topic(db.Model):
    __tablename__ = 'topic'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    
    name = db.Column(db.String(100), nullable=False)
    information = db.Column(db.String(200))
    creation_date = db.Column(db.DateTime, nullable = False, default=datetime.now)
    update_date = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    # Relationship
    log = db.relationship('Log', back_populates='topic', cascade='all, delete', lazy=True)

    def create_topic(name, information):
        new_topic = Topic(name = name,
                      information = information)

        return create_integrify(new_topic, Topic.__tablename__)
    