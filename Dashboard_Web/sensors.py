from flask import Blueprint, render_template, request, url_for

sensors = Blueprint("sensors", __name__, template_folder="templates")

sensors_list = ["DHT22", "HC-ST04"]

@sensors.route('/remove_sensor')
def remove_sensor():
    global sensors_list
    return render_template("listar_editar_remover.html", sensors=sensors_list)

@sensors.route('/del_sensor', methods=['GET', 'POST'])
def del_sensor():
    global sensors_list
    if request.method == 'POST':
        sensor_name = request.form['sensor_name']
    else:
        sensor_name = request.args.get('sensor_name', None)
    sensors_list.pop(sensor_name)
    return render_template("listar_editar_remover.html", sensors=sensors_list)