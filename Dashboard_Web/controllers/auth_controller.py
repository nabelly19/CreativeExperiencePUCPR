from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
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
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)

    return redirect(url_for('read.dashboard'))

@auth.route('/signup')
def signup():
    return render_template('registerUser.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    name = request.form.get('name')
    cpf = request.form.get('cpf')
    birth_date = request.form.get('birth_date')
    gender = request.form.get('gender')
    email = request.form.get('email')
    nickname = request.form.get('nickname')
    password = request.form.get('password')

    user = Users.query.filter_by(email=email).first()
    
    if user:
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    new_user = Users.create_user(
        name=name, 
        cpf=cpf, 
        birth_date=birth_date,
        gender=gender, 
        email=email, 
        nickname=nickname, 
        password=generate_password_hash(password, method='pbkdf2:sha256'))
    
    if not new_user["success"]:
        flash(", ".join(new_user["errors"]))
        return redirect(url_for('auth.signup'))

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('app.index'))
