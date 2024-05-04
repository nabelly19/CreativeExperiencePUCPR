from flask import *
from flask_mqtt import Mqtt
import json

# Objeto Flask
app = Flask(__name__)


app.config['MQTT_BROKER_URL'] = 'mqtt-dashboard.com'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''  # Set this item when you need to verify username and password
app.config['MQTT_PASSWORD'] = ''  # Set this item when you need to verify username and password
app.config['MQTT_KEEPALIVE'] = 5000  # Set KeepAlive time in seconds
app.config['MQTT_TLS_ENABLED'] = False  # If your broker supports TLS, set it True

mqtt_client= Mqtt()
mqtt_client.init_app(app)


# Rota principal
@app.route('/')
def dashboard():
    umidade = {'Umidade': '60%'}
    nivel = {'nível': 'BAIXO'}
    temperatura = {'Temperatura': '30º'}
    mensagem = {'Mensagem' : 'O NÍVEL DE ÁGUA ULTRAPASSOU O LIMITE, RISCOS DE ALAGAMENTO NA PRÓXIMA CHUVA!'}
    status = {'Status': 'DESLIGADO'}
    return render_template("dados.html", temperatura=temperatura, umidade=umidade, nivel=nivel, mensagem=mensagem, status=status)


@app.route('/publish_message', methods=['GET','POST'])
def publish_message():
    request_data = request.get_json()
    publish_result = mqtt_client.publish(request_data['topic'], request_data['message'])
    return jsonify(publish_result)



# Inicialização do aplicativo
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)