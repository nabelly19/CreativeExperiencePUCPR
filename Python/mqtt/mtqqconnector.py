import paho.mqtt.client as mqtt
import datetime
import time
import sys
import ssl
from influxdb import InfluxDBClient

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("/TOPICO_RAIZ_A_SER_LIDO/#")
    
def on_message(client, userdata, msg):
    print("Received a message on topic: " + msg.topic)
    # Use utc as timestamp
    receiveTime=datetime.datetime.utcnow()
    message=msg.payload.decode("utf-8")
    isfloatValue=False
    try:
        # Convert the string to a float so that it is stored as a number and not a string in the database
        val = float(message)
        isfloatValue=True
    except:
        print("Could not convert " + message + " to a float value")
        isfloatValue=False

    if isfloatValue:
        print(str(receiveTime) + ": " + msg.topic + " " + str(val))

        json_body = [
            {
                "measurement": msg.topic,
                "time": receiveTime,
                "fields": {
                    "value": val
                }
            }
        ]

        dbclient.write_points(json_body)
        print("Finished writing to InfluxDB")
        
# Set up a client for InfluxDB
dbclient = InfluxDBClient('127.0.0.1', 8086, 'USER', 'SENHA', 'BANCO')

# Initialize the MQTT client that should connect to the Mosquitto broker
client = mqtt.Client("Colector")
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set('USERNAME_MQTT','SENHA_MQTT')

client.tls_set('/CAMINHO_ABSOLUTO_DO_CA_CRT')
client.tls_insecure_set(True)

connOK=False
while(connOK == False):
    try:
        client.connect("IP_OU_URL_DO_BROKER", 443, 60)
        print("Ok")
        connOK = True
    except:
        connOK = False
        print("ops...")
    time.sleep(2)

# Blocking loop to the Mosquitto broker
client.loop_forever()


"'pip install paho-mqtt/pip install influxdb no terminal antes de execultar o codigo. lembre-se de trocar as portas de conexao'"