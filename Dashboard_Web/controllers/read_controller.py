from flask import Blueprint, request, render_template, redirect, url_for, flash
from models.iot.device import Device

read = Blueprint("read",__name__, template_folder="views")

@read.route('/devices_list')
def devices_list():
    device_type = ['Sensor', 'Atuador']
    all_devices = Device.read_devices_with_topics()

    if all_devices == None:
        flash('Sem registros no momento!')

    return render_template("devicesList.html", devices=all_devices, type=device_type)
