import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


load_dotenv()  # Carrega as variáveis do arquivo .env

db = SQLAlchemy()

db_name = os.getenv("DB_NAME")
db_password = os.getenv("DB_PASSWORD")
db_user = os.getenv("DB_USER")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")

instance = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
