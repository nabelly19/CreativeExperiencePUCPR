from controllers.app_controller import create_app
from utils.create_db import create_db

if __name__ == "__main__":
    app = create_app()
    print("Criando o Banco de Dados!")
    create_db(app)
    app.run(host='0.0.0.0', port=8080, debug=True)


# Debug=False > evita a duplicação dos dados 
# create_db(app) > se comentado não sobescreverá o banco de dados existente
