from flask import Blueprint, request, render_template, redirect, url_for, flash
from models.iot.device import Device
from models.iot.topic import Topic


devices = Blueprint("devices",__name__, template_folder="views")

@devices.route('/add_device')
def register_device():
    return render_template("registerDevice.html")


@devices.route('/add_device', methods=['POST'])
def add_device():
    name = request.form.get("device_name")
    brand = request.form.get("device_brand")
    type = request.form.get("device_type")
    title = request.form.get("topic_title")
    is_active = True if request.form.get("is_active") == "on" else False

    new_device = Device.create_device(name, brand, type, is_active)
    device_id = new_device["object"]
    new_topic = Topic.create_topic(title, device_id.id)

    if not new_device["success"] or not new_topic["success"]:
        #flash(", ".join(new_device["errors"]))
        return redirect(url_for('devices.add_device'))

    return redirect(url_for('devices.devices_list'))

@devices.route('/devices_list')
def devices_list():
    device_type = ['Sensor', 'Atuador']
    all_devices = Device.get_devices_with_topics()

    if not all_devices:
        flash('Sem registros no momento!')

    return render_template("devicesList.html", devices=all_devices, type=device_type)

@devices.route('/del_device')
def del_device():
    id = request.args.get('id', None)
    sensors = Device.delete_sensor(id)
    return redirect(url_for('devices.devices_list'))
