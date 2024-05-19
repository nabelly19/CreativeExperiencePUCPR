from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from models.user.users import Users
from models.db import db

auth = Blueprint('auth', __name__, template_folder="views")

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    nickname = request.form.get('nickname')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = Users.query.filter_by(nickname=nickname).first()

    #if not user or not check_password_hash(user.password, password): 
    #    flash('Please check your login details and try again.')
    #    return redirect(url_for('auth.login'))

    login_user(user, remember=remember)

    return redirect(url_for('main.dashboard'))

@auth.route('/signup')
def signup():
    return render_template('registerUser.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = Users.query.filter_by(email=email).first()
    
    if user:
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    new_user = Users(email=email, name=name, password=generate_password_hash(password, method='pbkdf2:sha256'))

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
