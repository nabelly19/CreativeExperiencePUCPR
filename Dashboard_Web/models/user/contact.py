from models import db
from models.db import datetime
from models.validate.integrity import create_with_integrity, update_with_integrity

#Contact class, atributes and methods. The "db" from our models.py is being imported in order to create the data base especifications
class Contact(db.Model):
    __tablename__ = 'contact'

    id= db.Column(db.Integer, autoincrement=True, primary_key=True)

    country_code = db.Column(db.SmallInteger, nullable=False, default=55)
    area_code = db.Column(db.SmallInteger, nullable=False)
    number = db.Column(db.Integer, nullable=False)
    update_date = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    # Foreign keys
    #user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationship
    #user = db.relationship('Users', back_populates='contact')
    
    #creation of the user's contact method
    def create_contact(country_code, area_code, number, user_id):
        new_contact = Contact(contry_code = country_code,
                              area_code = area_code,
                              number = number,                          
                              user_id = user_id)
        return create_with_integrity(new_contact, Contact.__tablename__)
    
    #function to find a specific contact
    def get_single_contact(number, area_code):
        contact = Contact.query.filter(
            Contact.area_code == area_code,
            Contact.number == number
        ).first()
        
        if contact is not None:
            return contact
        else:
            return None
    
    #method to return all the contacts listed on the DB
    def get_all_contacts():
        all_contacts = Contact.query.all()
        return all_contacts
    
    #function to update someone's contact
    def update_contact(new_area_code, new_number, old_number, old_area_code):
        contact = Contact.get_single_contact(old_number, old_area_code)
        
        if contact is not None:
            contact.area_code = new_area_code
            contact.number = new_number
        return update_with_integrity(contact, Contact.__tablename__)
