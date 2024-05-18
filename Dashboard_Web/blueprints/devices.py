from flask import Blueprint, render_template, request, url_for, redirect

devices = Blueprint("devices", __name__, template_folder="templates")

actuators_list = ["Led", "Servo Motor"]
sensors_list = ["DHT22", "HC-ST04"]

@devices.route('/register_devices')
def register_devices():
    return render_template("addHardware.html")

@devices.route('/add_device', methods=['POST', 'GET'])
def add_device():
    global actuators_list, sensors_list
    if request.method == 'POST':
        device_name = request.form['device_name']
        device_type = request.form['device_type']
    else:
        device_name = request.args.get('device_name', None)
        device_type = request.args.get['device_type', None]
    if device_type == 'sensor':
        device_name = device_name.upper()
        sensors_list.append(device_name)
    elif device_type == 'actuator':
        device_name = device_name.upper()
        actuators_list.append(device_name)
    return redirect("/devices_list")

@devices.route('/devices_list')
def devices_list():
    global actuators_list, sensors_list
    return render_template("devicesList.html", actuators=actuators_list, sensors=sensors_list)

@devices.route('/del_device', methods=['GET', 'POST'])
def del_device():
    global sensors_list, actuators_list
    if request.method == 'POST':
        device_name = request.form['validation']
        device_name = device_name.upper()
    else:
        device_name = request.args.get('validation', None)
    if device_name in sensors_list:
        sensors_list.remove(device_name)
    elif device_name in actuators_list:
        actuators_list.remove(device_name)
    return redirect("/devices_list")