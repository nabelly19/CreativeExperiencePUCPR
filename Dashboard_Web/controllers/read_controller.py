from flask import Blueprint, request, render_template, redirect, url_for, flash, jsonify
from flask_login import login_required
from models.iot.log import Log

read = Blueprint("read",__name__, template_folder="views")

# APAGAR DEPOIS -------------------------------------------
temperature = 0
humidity = 0
mensagem_de_alerta = ""
alerta_value = 0
botao_value = 0
mensagem_nivel_da_agua = ""
#-----------------------------------------------------------

@read.route('/dashboard')
#@login_required
def dashboard():
    global temperature, humidity, mensagem_de_alerta, mensagem_nivel_da_agua, alerta_value
    values = {"Temperatura":temperature, "Umidade":humidity, "Mensagem de alerta":mensagem_de_alerta, "Nível da água":mensagem_nivel_da_agua, "Status do alarme":alerta_value}
    return render_template("dashboard.html", values=values)

@read.route('/logs')
#@login_required
def logs():
    all_logs = Log.get_logs_with_data()

    #if not all_logs:
        #flash('Sem registros no momento!')

    return render_template("logs.html", logs=all_logs)


@read.route('/realTimeData', methods= ['GET'])
def any():
    values = {"Temperatura":temperature, "Umidade":humidity, "Mensagem de alerta":mensagem_de_alerta, "Nível da água":mensagem_nivel_da_agua, "Status do alarme":alerta_value}
    return jsonify(values)

'''@read.route('/register_log')
#@login_required
def register_log(data, topic):
    return'''