from models import db
from models.db import datetime
from models.iot.device import Device
from models.iot.topic import Topic
from sqlalchemy.orm import joinedload
from models.validate.integrity import create_with_integrity


class Log(db.Model):
    __tablename__ = 'log'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    
    information = db.Column(db.String(200))
    creation_date = db.Column(db.DateTime, nullable = False, default=datetime.now)

    # Foreign Key
    topic_id= db.Column(db.Integer, db.ForeignKey('topic.id', ondelete='SET NULL'), nullable=True)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id', ondelete='SET NULL'), nullable=True)

    # Relationships
    topic = db.relationship('Topic', foreign_keys=[topic_id], back_populates='log', lazy=True, uselist=False)
    device = db.relationship('Device', foreign_keys=[device_id], back_populates='log', lazy=True, uselist=False)

    def get_logs_with_data(start_date, end_date):
        all_logs = (Log.query
                    .filter(Log.creation_date >= start_date)
                    .filter(Log.creation_date <= end_date)
                    .options(joinedload(Log.topic),
                    joinedload(Log.device))
                    .all())
        
        return all_logs

    def save_log(topic_name, information):
        topic_result = Topic.get_single_topic(topic_name)
        device_result = Device.get_single_device(topic_result.device_id)
        if (topic_result is not None) and (device_result.is_active == True):
            new_log = Log(information = information, 
                          topic_id = topic_result.id, 
                          device_id = device_result.id)
            
            return create_with_integrity(new_log, Log.__tablename__)

    def get_logs_for_topic(topic_id, start_date, end_date):
        logs = (Log.query.join(Topic)
                .filter(Topic.id == topic_id)
                .filter(Log.creation_date >= start_date)
                .filter(Log.creation_date <= end_date)
                .options(joinedload(Log.topic))
                .all())
        
        return logs

    def get_logs_for_device(device_name, start_date, end_date):
        logs = (Log.query.join(Device)
                .filter(Device.name == device_name)
                .filter(Log.creation_date >= start_date)
                .filter(Log.creation_date <= end_date)
                .options(joinedload(Log.device))
                .all())
        
        return logs