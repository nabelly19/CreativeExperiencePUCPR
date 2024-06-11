#file to manipulate the creation and manipulation of the data base.
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

load_dotenv()  #Load the .env file variables

db = SQLAlchemy() #incialize the data base variable, will be used on all the db files

db_name = os.getenv("DB_NAME")
db_password = os.getenv("DB_PASSWORD")
db_user = os.getenv("DB_USER")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")

instance = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
