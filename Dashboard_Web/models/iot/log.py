from models import db
from models.db import datetime, timedelta
from models.iot.device import Device
from models.iot.topic import Topic
from sqlalchemy.orm import joinedload
from sqlalchemy import func, cast, Date, Float
from models.validate.integrity import create_with_integrity

#Log class, atributes and methods. The "db" from our models.py is being imported in order to create the data base especifications
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

    def save_log(topic_name, information, data):
        topic_result = Topic.get_single_topic(topic_name)
        device_result = Device.get_single_device(topic_result.device_id)
        if (topic_result is not None) and (device_result.is_active == True):
            new_log = Log(information = information, 
                          creation_date = data,
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
    
    def get_logs_media():
        # Define o nome do tópico que estamos interessados
        topic_name = '/Temperatura'

        # Define a data de hoje e os dias anteriores
        today = datetime.now()
        four_days_ago = today - timedelta(days=4)

        # Consulta para calcular a média da temperatura para cada um dos quatro dias anteriores
        results = (db.session.query(
                        cast(Log.creation_date, Date).label('date'),
                        func.avg(cast(Log.information, Float)).label('avg_temperature')
                )
                .join(Topic, Log.topic_id == Topic.id)
                .filter(
                    Topic.name == topic_name,
                    Log.creation_date >= four_days_ago,
                    Log.creation_date < today
                )
                .group_by(cast(Log.creation_date, Date))
                .order_by(cast(Log.creation_date, Date))
            .all())
    
        return results