import paho.mqtt.client as mqtt 
from random import randrange, uniform
import time

# Variáveis com os tópicos utilizados
myTopicTemperatura = "/Temp/infLed"
myTopicUmidade = "/Umid/infLed" 
myTopicAction = "/Action/Buzzer"

# Variáveis que receberão os valores de temp. e umid. do sensor DHT22 (Wokwi)
temperature = 0.0
humidity = 0.0

# Conexão com o Broker
mqttBroker ="broker.hivemq.com" 

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(mqttBroker) 

# Esta função analisa o tópico que deverá ser escutado e armazena o conteúdo do tópico (payload) em uma variável
def callback(client, userdata, message):
    global myTopicTemperatura, myTopicUmidade, temperature, humidity

    print("Tópico: ", str(message.topic))
    if (message.topic == myTopicTemperatura):
               temperature = int(str(message.payload.decode("utf-8"))) 
    if (message.topic == myTopicUmidade):
                humidity = int(str(message.payload.decode("utf-8")))
    
# Indica o assunto de cada tópico
#print("Temperatura: " + str(myTopicTemperatura))
#print("Umidade: " + str(myTopicUmidade))
    
client.message_callback_add("/Temp/infLed", callback)
client.subscribe("/Temp/infLed")

client.message_callback_add("/Umid/infLed", callback)
client.subscribe("/Umid/infLed")

# Aqui haverá as comparações (previsão de chuva), de acordo com as informações nos tópicos do Broker. A partir daí, serão publicados no respectivo tópico as ações a serem tomadas na ESP32
while True:
    client.loop()

    # Utilizar apenas para testar e vizualizar as informações que estão sendo revebidas do broker.
    #print("Umidade recebida: ", humidity)
    #print("Temperatura recebida", temperature)

    # Se alta umidade e temperatura baixa, então chove
    if humidity > 70 and temperature < 20:
        client.loop()
        client.publish(myTopicAction, '0') # Não ativar alarme
        print("Provavelmente choverá!")
    # Se alta umidade e temperatura alta, então chove (chuva forte)
    elif humidity > 70 and temperature > 25:
        client.loop()
        client.publish(myTopicAction, '1') # Ativar alarme
        print("Provavelmente choverá forte!")
    # Se baixa umidade e temperatura baixa, então não chove
    elif humidity < 60 and temperature < 20:
        client.loop()
        client.publish(myTopicAction, '0') # Não ativar alarme
        print("Provavelmente não choverá!")
    # Se baixa umidade e temperatura alta, então não chove
    elif humidity < 60 and temperature > 25:
         client.loop()
         client.publish(myTopicAction, '0') # Não ativar alarme
         print("Provavelmente chuva leve!")
    else:
        client.loop()
        client.publish(myTopicAction, '0') # Não ativar alarme
        print("Provavelmente chuva leve!")

    time.sleep(10)
        
        
    
