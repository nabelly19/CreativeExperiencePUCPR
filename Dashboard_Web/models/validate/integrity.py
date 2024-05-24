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
            result = Log.save_log(myTopic, value)
            return print(result)
    except:
        pass

# O Mateus que escreveu isso...
def update_with_integrity(object, tablename):
    tablename = str(tablename).upper()
    try:
        db.session.commit()
        return {"success": True, "object": object}
    except Exception as e:
        db.session.rollback()
        return {"success": False, 
                "errors": [str(e), f"Erro ao cadastrar {tablename} no banco de dados!"]}
'''
    def create_device(name, brand, type, is_active):
        new_device = Device(name = name, 
                        brand = brand, 
                        type = type, 
                        is_active = is_active)
        
        return create_with_integrity(new_device, Device.__tablename__)


'''
