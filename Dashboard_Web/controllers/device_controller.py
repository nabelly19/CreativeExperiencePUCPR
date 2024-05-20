from flask import Blueprint, request, render_template, redirect, url_for, flash
from models.iot.device import Device

devices = Blueprint("devices",__name__, template_folder="views")

@devices.route('/add_device')
def register_device():
    return render_template("registerDevice.html")


@devices.route('/add_device', methods=['POST'])
def add_device():
    name = request.form.get("device_name")
    brand = request.form.get("device_brand")
    type = request.form.get("device_type")
    is_active = True if request.form.get("is_active") == "on" else False

    new_device = Device.create_device(name, brand, type, is_active)

    if not new_device["success"]:
        flash(", ".join(new_device["errors"]))
        return redirect(url_for('auth.signup'))

    return redirect(url_for('main.index')) # MUDAR O REDIRECIONAMENTO