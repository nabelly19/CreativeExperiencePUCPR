# app.py
# pip install flask-mqtt
# pip install flask-socketio
#08/05/2024 - Josiel

from flask import Flask, render_template, request, redirect, url_for,jsonify
from login import login
from devices import devices
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
import json
from time import sleep
#https://wokwi.com/projects/394918938756685825

temperature = 0
humidity = 0
mensagem_de_alerta = ""
alerta_value = 0
botao_value = 0
mensagem_nivel_da_agua = ""

app= Flask(__name__)
## __name__ is the application name
SocketIO = SocketIO(app)

app.register_blueprint(login, url_prefix='/')
app.register_blueprint(devices, url_prefix='/')


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

@app.route('/')
def index():
    return render_template("home.html")

@app.route('/logoff')
def logoff():
    return render_template("login.html")

@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/dashboard') 
def dashboard():
    return render_template("dashboard.html")

@app.route('/realTimeData', methods= ['GET'])
def any():
    values = {"Temperatura":temperature, "Umidade":humidity, "Mensagem de alerta":mensagem_de_alerta, "Nível da água":mensagem_nivel_da_agua, "Status do alarme":alerta_value}
    values_json = json.dumps(values, ensure_ascii=False)
    return jsonify(result = values_json)

### FALTA TRANSFERIR - 18/05 -> COLOCAR NO ARQUIVO DO ACTUATOR_CONTROLLER
'''@app.route('/action_alert', methods=['POST'])
def action_alert():
    global alerta_value

    if alerta_value == 'Ligado': # Caso o botão esteja ligado, então publicar para que ele desligue
        mqtt_client.publish(myTopicButton, '0')
    elif alerta_value == 'Desligado': # Caso o botão esteja desligado, então publicar para que ele ligue
        mqtt_client.publish(myTopicButton, '1')   
    return redirect('/dashboard')'''


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
    if(message.topic==myTopicTemperatura):
        global temperature
        temperature = message.payload.decode()
    if(message.topic==myTopicUmidade):
        global humidity
        humidity = message.payload.decode()
    if(message.topic==myTopicMensagem):
        global mensagem_de_alerta
        mensagem_de_alerta = message.payload.decode()
    if(message.topic==myTopicAction):
        global alerta_value
        alerta_value = message.payload.decode()
        if alerta_value == '0':
            alerta_value = "Desligado"
        elif alerta_value == "1":
            alerta_value = "Ligado"
    if(message.topic==myTopicButton):
        global botao_value
        botao_value = message.payload.decode()
    if(message.topic==myTopicWaterLevel):
        global mensagem_nivel_da_agua
        mensagem_nivel_da_agua = message.payload.decode()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True) 