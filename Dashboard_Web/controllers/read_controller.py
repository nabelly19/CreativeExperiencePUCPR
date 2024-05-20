from flask import Blueprint, request, render_template, redirect, url_for

read = Blueprint("sensor_",__name__, template_folder="views")

@read.route('/device_list')
def device_list():
    return redirect(url_for('main.index'))
