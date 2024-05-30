from models import db
from models.db import datetime
from models.validate.integrity import create_with_integrity, update_with_integrity

#Topic class, atributes and methods. The "db" from our models.py is being imported in order to create the data base especifications
class Topic(db.Model):
    __tablename__ = 'topic'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    title = db.Column(db.String(100), nullable=False, unique=True)
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
        
    def get_all_topics():
        all_topics = Topic.query.all()
        return all_topics

    def update_topic(new_title, old_title):
        topic = Topic.get_single_topic(old_title)
        
        if topic is not None:
            topic.title = new_title

            return update_with_integrity(topic, Topic.__tablename__)
