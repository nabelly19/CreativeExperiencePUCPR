import paho.mqtt.client as mqtt
import time

# Callback para quando o cliente se conectar ao broker MQTT
def on_connect(client, userdata, flags, rc):
    print("Conectado ao broker com código de resultado: " + str(rc))
    # Subscreva a um tópico quando conectado com sucesso
    client.subscribe("meu/topico")

# Callback para quando uma mensagem for recebida do broker MQTT
def on_message(client, userdata, msg):
    print("Mensagem recebida no tópico '" + msg.topic + "': " + str(msg.payload))

# Configuração do cliente MQTT
client = mqtt.Client()

# Definindo os callbacks
client.on_connect = on_connect
client.on_message = on_message

# Conectando ao broker MQTT
client.connect("broker.mqtt.com", 1883, 60)  # Substitua "broker.mqtt.com" pelo endereço do seu broker MQTT

# Mantendo a conexão
client.loop_start()

# Publicando uma mensagem em um tópico
client.publish("meu/topico", "Olá, mundo!")

# Mantenha o script em execução para continuar recebendo mensagens
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Desconectando...")
    client.disconnect()
    client.loop_stop()


"'pip install paho-mqtt no terminal antes de execultar o codigo. lembre-se de trocar as portas de conexao'"