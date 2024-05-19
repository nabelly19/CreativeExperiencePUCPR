from flask import Blueprint, request, render_template, redirect, url_for
from models.iot.device import Device

sensor_ = Blueprint("sensor_",__name__, template_folder="views")

@sensor_.route('/register_sensor')
def register_sensor():
    return render_template("register_sensor.html")


@sensor_.route('/add_sensor', methods=['POST'])
def add_sensor():
    name = request.form.get("name")
    brand = request.form.get("brand")
    model = request.form.get("type")
    is_active = True if request.form.get("is_active") == "on" else False

    Device.add_sensor(name, brand, model, is_active)

    return redirect(url_for('home.html'))