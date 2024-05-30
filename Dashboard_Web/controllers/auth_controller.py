from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, login_required

from models.user.users import Users
from models.user.admin import Admin
from models.user.role import Role


auth = Blueprint('auth', __name__, template_folder="views")

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    nickname = request.form.get('nickname')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = Users.get_single_user(nickname)

    if not user or not check_password_hash(user.password, password): 
        flash('Credenciais inválidas, verifique seu usuário ou senha!')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)

    return redirect(url_for('read.dashboard'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
