from flask import Blueprint, request, render_template, redirect, url_for
from models.iot.device import Device

read = Blueprint("read",__name__, template_folder="views")

@read.route('/devices_list')
def devices_list():
    all_devices = Device.read_devices()
    return render_template("devicesList.html", devices=all_devices)
