from flask import Flask, render_template, request
from models.db import db, instance
from controllers.sensors_controller import sensor_
from controllers.reads_controller import read, Read
from flask_mqtt import Mqtt
import json


def create_app():
    app = Flask(__name__,
        template_folder="./views/",
        static_folder="./static/",
        root_path="./")
    
    app.config['TESTING'] = False
    app.config['SECRET_KEY'] = 'generated-secrete-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = instance
    db.init_app(app)

    app.register_blueprint(sensor_, url_prefix='/')
    app.register_blueprint(read, url_prefix='/')
    
    @app.route('/')
    def index():
        return render_template("home.html")
    
    app.config['MQTT_BROKER_URL'] = 'mqtt-dashboard.com'
    app.config['MQTT_BROKER_PORT'] = 1883
    app.config['MQTT_USERNAME'] = '' # Set this item when you need to verify username and password
    app.config['MQTT_PASSWORD'] = '' # Set this item when you need to verify username and password
    app.config['MQTT_KEEPALIVE'] = 5000 # Set KeepAlive time in seconds
    app.config['MQTT_TLS_ENABLED'] = False # If your broker supports TLS, set it True
    mqtt_client= Mqtt()
    mqtt_client.init_app(app)
    topic_subscribe = "/aula_flask/"


    @mqtt_client.on_connect()
    def handle_connect(client, userdata, flags, rc):
        if rc == 0:
            print('Broker Connected successfully')
            mqtt_client.subscribe(topic_subscribe) # subscribe topic
        else:
            print('Bad connection. Code:', rc)


    @mqtt_client.on_message()
    def handle_mqtt_message(client, userdata, message):
        if(message.topic==topic_subscribe):
            js = json.loads(message.payload.decode())
            print(js)
            try:
                with app.app_context():
                    Read.save_read(js["sensor"],js["valor"])
            except:
                pass


    return app
