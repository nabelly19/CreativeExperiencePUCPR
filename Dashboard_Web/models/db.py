from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db= SQLAlchemy()

bd_name = "FloodPrevention"
password = "pss" # Gerar hash dessa senha

instance = f"mysql+pymysql://root:{password}@localhost:3306/{bd_name}"
