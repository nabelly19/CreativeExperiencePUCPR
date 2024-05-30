from models import db

# Validar a criação de uma nova instância passada no parâmetro
def create_with_integrity(object, tablename):
    tablename = str(tablename).upper()
    try:
        db.session.add(object)
        db.session.commit()
        return {"success": True, "object": object}
    except Exception as e:
        db.session.rollback()
        return {"success": False, 
                "errors": [str(e), f"Erro ao cadastrar {tablename} no banco de dados!"]}

def save_with_integrity(app, myTopic, value):
    from models.iot.log import Log    
    try:
        with app.app_context():
            Log.save_log(myTopic, value)
    except:
        pass

def update_with_integrity(object, tablename):
    tablename = str(tablename).upper()
    try:
        db.session.commit()
        return {"success": True, "object": object}
    except Exception as e:
        db.session.rollback()
        return {"success": False, 
                "errors": [str(e), f"Erro ao cadastrar {tablename} no banco de dados!"]}

def delete_with_integrity(object, tablename):
    tablename = str(tablename).upper()
    try:
        db.session.delete(object)
        db.session.commit()
        return {"success": True, "object": object}
    except Exception as e:
        db.session.rollback()
        return {"success": False, 
                "errors": [str(e), f"Erro ao deletar {tablename} no banco de dados!"]}
