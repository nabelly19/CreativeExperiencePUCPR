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
    