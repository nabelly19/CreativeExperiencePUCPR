from flask import Blueprint, request, render_template, redirect, url_for, flash, jsonify
from flask_login import login_required
from models.iot.log import Log
from models.iot.topic import Topic
from models.iot.device import Device
from models.db import datetime
from controllers.auth_controller import roles_required


read = Blueprint("read",__name__, template_folder="views")

# ----------------------------------------------------------
# temperature = 0
# humidity = 0
# mensagem_de_alerta = ""
# alerta_value = 0
# botao_value = 0
# mensagem_nivel_da_agua = ""
# ----------------------------------------------------------

# @read.route('/dashboard')
# @login_required
# def dashboard():
#     global temperature, humidity, mensagem_de_alerta, mensagem_nivel_da_agua, alerta_value
#     values = {"Temperatura":temperature, "Umidade":humidity, "Mensagem de alerta":mensagem_de_alerta, "Nível da água":mensagem_nivel_da_agua, "Status do alarme":alerta_value}
#     return render_template("dashboard.html", values=values)

@read.route('/logs', methods=['GET', 'POST'])
@login_required
@roles_required('Estatístico', 'Root', 'Operador')
#@roles_required('Root')
#@roles_required('Operador')
def logs():
    all_topics = Topic.get_all_topics()
    all_devices = Device.get_all_devices_distinct()

    topic_id = request.form.get('topic')
    device_name = request.form.get('device')
    start_date = request.form.get('datetime_inicial')
    end_date = request.form.get('datetime_final')

    # Converte as datas para datetime, se necessário
    if start_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%dT%H:%M')
    if end_date:
        end_date = datetime.strptime(end_date, '%Y-%m-%dT%H:%M')

    try:
        # Filtrar por log.id
        if topic_id and topic_id != 'todos':
            logs = Log.get_logs_for_topic(topic_id, start_date, end_date)
            return render_template("logs.html", topics=all_topics, devices=all_devices, logs_topics=logs)

        # Filtrar por device.name
        elif device_name and device_name != 'todos':
            logs = Log.get_logs_for_device(device_name, start_date, end_date)
            return render_template("logs.html", topics=all_topics, devices=all_devices, logs_devices=logs)

        elif device_name == 'todos' or topic_id == 'todos':
            logs = Log.get_logs_with_data(start_date, end_date)
            return render_template("logs.html", topics=all_topics, devices=all_devices, logs_devices=logs)
        
        else:
            flash('Selecione os parâmetros de pesquisa!')

    except:
        flash('Sem registros no momento!')
        
    return render_template("logs.html", topics=all_topics, devices=all_devices)


# @read.route('/realTimeData', methods= ['GET'])
# @login_required
# def any():
#     values = {"Temperatura":temperature, "Umidade":humidity, "Mensagem de alerta":mensagem_de_alerta, "Nível da água":mensagem_nivel_da_agua, "Status do alarme":alerta_value}
#     return jsonify(values)
