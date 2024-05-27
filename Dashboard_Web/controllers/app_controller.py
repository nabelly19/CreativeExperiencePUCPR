from flask import Flask, redirect, render_template
from flask_login import LoginManager
from models.db import db, instance
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from models.validate.integrity import *

# Importação dos BLUEPRINTS
from controllers.auth_controller import auth
from controllers.device_controller import devices
from controllers.read_controller import read
from controllers.user_controller import users

#https://wokwi.com/projects/394918938756685825

temperature = 0
humidity = 0
mensagem_de_alerta = ""
alerta_value = 0
botao_value = 0
mensagem_nivel_da_agua = ""


def create_app():
    app = Flask(__name__,
        template_folder="./views/",
        static_folder="./static/",
        root_path="./")
    
    app.config['TESTING'] = False
    app.config['SECRET_KEY'] = 'generated-secrete-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = instance
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from models.user.users import Users
    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return Users.query.get(int(user_id))

    # Blueprints --------------------------------------------------------------------------------------
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(devices, url_prefix='/')
    app.register_blueprint(read, url_prefix='/')
    app.register_blueprint(users, url_prefix='/')

    @app.route('/')
    def index():
        return render_template("home.html")

    @app.route('/action_alert', methods=['POST'])
    def action_alert():
        global alerta_value

        if alerta_value == 'Ligado': # Caso o botão esteja ligado, então publicar para que ele desligue
            mqtt_client.publish(myTopicButton, '0')
        elif alerta_value == 'Desligado': # Caso o botão esteja desligado, então publicar para que ele ligue
            mqtt_client.publish(myTopicButton, '1')   
        return redirect('/dashboard')
    
    app.config['MQTT_BROKER_URL'] = 'mqtt-dashboard.com'
    app.config['MQTT_BROKER_PORT'] = 1883
    app.config['MQTT_USERNAME'] = ''  # Set this item when you need to verify username and password
    app.config['MQTT_PASSWORD'] = ''  # Set this item when you need to verify username and password
    app.config['MQTT_KEEPALIVE'] = 5000  # Set KeepAlive time in seconds
    app.config['MQTT_TLS_ENABLED'] = False  # If your broker supports TLS, set it True

    mqtt_client= Mqtt()
    mqtt_client.init_app(app)

    # Variáveis com os tópicos utilizados
    myTopicTemperatura = "/Temperatura"
    myTopicUmidade = "/Umidade" 
    myTopicMensagem = "/Mensagem/alerta"
    myTopicAction = "/Action/alerta"
    myTopicButton = "/Botao/alerta"
    myTopicWaterLevel = "/mensagem/nivelDaAgua"

    # Configuração da conexão com o broker (tópicos)
    @mqtt_client.on_connect()
    def handle_connect(client, userdata, flags, rc):
        if rc == 0:
            print('Broker Connected successfully')
            mqtt_client.subscribe(myTopicTemperatura) # subscribe topic
            mqtt_client.subscribe(myTopicUmidade) # subscribe topic
            mqtt_client.subscribe(myTopicMensagem) # subscribe topic
            mqtt_client.subscribe(myTopicAction) # subscribe topic
            mqtt_client.subscribe(myTopicButton) # subscribe topic
            mqtt_client.subscribe(myTopicWaterLevel) # subscribe topic
        else:
            print('Bad connection. Code:', rc)

    @mqtt_client.on_disconnect()
    def handle_disconnect(client, userdata, rc):
        print("Disconnected from broker")

    # Callback, escuta as informações vindas dos tópicos do broker
    @mqtt_client.on_message()
    def handle_mqtt_message(client, userdata, message):
        #print(message.payload.decode())

        if(message.topic==myTopicTemperatura):
            global temperature
            temperature = message.payload.decode()
            save_with_integrity(app, myTopicTemperatura, temperature)

        if(message.topic==myTopicUmidade):
            global humidity
            humidity = message.payload.decode()
            save_with_integrity(app, myTopicUmidade, humidity)

        if(message.topic==myTopicMensagem):
            global mensagem_de_alerta
            mensagem_de_alerta = message.payload.decode()
            save_with_integrity(app, myTopicMensagem, mensagem_de_alerta)

        if(message.topic==myTopicAction):
            global alerta_value
            alerta_value = message.payload.decode()
            if alerta_value == '0':
                alerta_value = "Desligado"
                save_with_integrity(app, myTopicAction, alerta_value)
            elif alerta_value == "1":
                alerta_value = "Ligado"
                save_with_integrity(app, myTopicAction, alerta_value)

        # EXCLUIR ELE 
        if(message.topic==myTopicButton):
            global botao_value
            botao_value = message.payload.decode()
            save_with_integrity(app, myTopicButton, botao_value)

        if(message.topic==myTopicWaterLevel):
            global mensagem_nivel_da_agua
            mensagem_nivel_da_agua = message.payload.decode()
            save_with_integrity(app, myTopicWaterLevel, mensagem_nivel_da_agua)

    return app
