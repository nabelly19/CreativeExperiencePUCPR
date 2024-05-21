from flask import Blueprint, request, render_template, redirect, url_for, flash
from models.iot.device import Device

read = Blueprint("read",__name__, template_folder="views")

@read.route('/devices_list')
def devices_list():
    device_type = ['Sensor', 'Atuador']
    all_devices = Device.get_sensors_with_topics()

    if not all_devices:
        flash('Sem registros no momento!')

    return render_template("devicesList.html", devices=all_devices, type=device_type)
