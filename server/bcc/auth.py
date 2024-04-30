from flask import (
    Flask, Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from login import login
from addsensors import register_sensor, register_actuator
from useradd import register
from editremoveusers import edit_user, delete_user

app = Flask(__name__)

bp = Blueprint('home', __name__, url_prefix='/home')

@bp.route('/', methods=('GET', 'POST'))
def register():
    return render_template('index.html')
