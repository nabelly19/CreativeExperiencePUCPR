# app.py
# pip install flask-mqtt
# pip install flask-socketio

from flask import Flask, render_template, request, redirect, url_for,jsonify
from login import login
from sensors import sensors
from actuators import actuators
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
import json

#https://wokwi.com/projects/394918938756685825

actuators_list = ["Led", "Servo Motor"]
sensors_list = ["DHT22", "HC-ST04"]

temperature = 0
humidity = 0
mensagem_de_alerta = ""
alerta_value = 0
botao_value = 0
mensagem_nivel_da_agua = ""

app= Flask(__name__)
## __name__ is the application name

app.register_blueprint(login, url_prefix='/')
app.register_blueprint(sensors, url_prefix='/')
app.register_blueprint(actuators, url_prefix='/')


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

@app.route('/register_devices')
def register_devices():
    return render_template("addHardware.html")

@app.route('/add_device', methods=['POST', 'GET'])
def add_device():
    global actuators_list, sensors_list
    if request.method == 'POST':
        device_name = request.form['device_name']
        device_type = request.form['device_type']
    else:
        device_name = request.args.get('device_name', None)
        device_type = request.args.get['device_type', None]
    if device_type == 'sensor':
        sensors_list.append(device_name)
    elif device_type == 'actuator':
        actuators_list.append(device_name)
    return redirect("/devices_list")

@app.route('/devices_list')
def devices_list():
    global actuators_list, sensors_list
    return render_template("devicesList.html", actuators=actuators_list, sensors=sensors_list)

@app.route('/dashboard') 
def dashboard():
    global temperature, humidity, mensagem_de_alerta, mensagem_nivel_da_agua, alerta_value
    values = {"Temperatura":temperature, "Umidade":humidity, "Mensagem de alerta":mensagem_de_alerta, "Nível da água":mensagem_nivel_da_agua, "Status do alarme":alerta_value}
    return render_template("dashboard.html", values=values)


# publicar em um tópico a partir da interface web. Configurar esta parte lá no HTML da dashboard, para que quando o botão seja precionado (ligar/desligar) a mesnsagem seja encaminhada para esta rota, afim de enviar ao tópico de "/Botao/alerta", parando ou ligando o sistema IOT.
@app.route('/publish_message', methods=['GET','POST'])
def publish_message():
    request_data = request.get_json()
    publish_result = mqtt_client.publish(request_data['topic'], request_data['message'])
    return jsonify(publish_result)

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
    print(message.payload.decode())
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