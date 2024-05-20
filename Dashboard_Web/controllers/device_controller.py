from flask import Blueprint, request, render_template, redirect, url_for
from models.iot.device import Device

devices = Blueprint("sensor_",__name__, template_folder="views")

@devices.route('/add_device')
def register_sensor():
    return render_template("register_sensor.html")


@devices.route('/add_device', methods=['POST'])
def add_device():
    name = request.form.get("name")
    brand = request.form.get("brand")
    type = request.form.get("type")
    is_active = True if request.form.get("is_active") == "on" else False

    Device.create_device(name, brand, type, is_active)

    return redirect(url_for('devices.add_device'))