from models import db
from models.db import datetime
from models.validate.integrity import create_with_integrity, update_with_integrity

class Client(db.Model):
    __tablename__ = 'client'

    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    
    creation_date = db.Column(db.DateTime, nullable=False)

    # Relationship
    user = db.relationship('Users', back_populates='client', lazy=True)

#function to create a new client
def create_client(user_id):
    new_client = Client(id=user_id,
                        creation_date = datetime.now()    
                        )
    
    return create_with_integrity(new_client, Client.__tablename__)

#function to get a specif client
def get_single_client(user_id):
    client = Client.filter(Client.id == user_id).first()
    return client

#returning all clients method
def get_all_clients():
    all_clients = Client.query.all()
    return all_clients

def update_client(user_id, new_creation_date=None):
    client = get_single_client(user_id)
    
    if client is not None:
        if new_creation_date is not None:
            client.creation_date = new_creation_date
            client.update_date = datetime.now()
    
    return update_with_integrity()

