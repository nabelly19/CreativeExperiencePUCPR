from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from functools import wraps

from models.user.users import Users


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


def roles_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return abort(401)  # Not authenticated

            if current_user.admin is None or current_user.admin.role is None:
                return abort(403)  # Forbidden

            user_role = current_user.admin.role.name

            if user_role not in roles:
                return abort(403)  # Forbidden

            return f(*args, **kwargs)
        return decorated_function
    return decorator