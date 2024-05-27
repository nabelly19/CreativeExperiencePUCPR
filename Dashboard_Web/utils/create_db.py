from flask import Flask
from models import *

def create_db(app:Flask):
    with app.app_context():
        #db.drop_all() # Apagar todos os dados sempre que a  aplicação é reiniciada
        db.create_all() # Criar o banco de dados com todas as tabelas
       