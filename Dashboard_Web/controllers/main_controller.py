from flask import Blueprint, render_template
from flask_login import login_required

main = Blueprint('main', __name__, template_folder="views")

temperature = 0
humidity = 0
mensagem_de_alerta = ""
alerta_value = 0
botao_value = 0
mensagem_nivel_da_agua = ""

@main.route('/')
def index():
    return render_template("home.html")

@main.route('/home')
def home():
    return render_template("home.html")

@main.route('/dashboard')
@login_required
def dashboard():
    global temperature, humidity, mensagem_de_alerta, mensagem_nivel_da_agua, alerta_value
    values = {"Temperatura":temperature, "Umidade":humidity, "Mensagem de alerta":mensagem_de_alerta, "Nível da água":mensagem_nivel_da_agua, "Status do alarme":alerta_value}
    return render_template("dashboard.html", values=values)
