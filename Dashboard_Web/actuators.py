from flask import Blueprint, Flask, render_template, request

actuators = Blueprint("actuators", __name__, template_folder = "template")

actuators_list = ["Led", "Servo Motor"]

#@actuators.route('/register_actuator')
#def register_actuator():
#    return render_template('cadastro_sensors_actuators.html')

#@actuators.route('/add_actuator', methods=['POST', 'GET'])
#def add_actuator():
#    global actuators_list
#    if request.method == 'POST':
#        actuator_name = request.form['actuator_name']
#        actuator_value = request.form['actuator_value']
#    else:
#        actuator_name = request.args.get('actuator_name', None)
#        actuator_value = request.args.get('actuator_value', None)
#    actuators_list[actuator_name] = actuator_value
#    return render_template('listar_editar_remover.html', actuators=actuators_list)

# @actuators.route('/list_actuators')
# def list_actuators():
#    return render_template('listar_editar_remover.html', actuators=actuators_list)

@actuators.route('/remove_actuator')
def remove_actuator():
    global actuators_list
    return render_template("listar_editar_remover.html", actuators=actuators_list)

@actuators.route('/del_actuator', methods=['GET', 'POST'])
def del_actuator():
    global actuators_list
    if request.method == 'POST':
        actuator_name = request.form['actuator_name']
    else:
        actuator_name = request.args.get('actuator_name', None)
    actuators_list.pop(actuator_name)
    return render_template("listar_editar_remover.html", actuators=actuators_list)