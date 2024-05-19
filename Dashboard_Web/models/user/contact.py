from models import db
from models.db import datetime

class Contact(db.Model):
    __tablename__ = 'contact'

    id= db.Column(db.Integer, autoincrement=True, primary_key=True)

    country_code = db.Column(db.SmallInteger, nullable=False, default=55)
    area_code = db.Column(db.SmallInteger, nullable=False)
    number = db.Column(db.Integer, nullable=False)
    update_date = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationship
    user = db.relationship('Users', back_populates='contact')
