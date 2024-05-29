from flask import Blueprint, request, render_template, redirect, url_for, flash
from models.user.users import Users
from models.user.client import Client
from models.user.admin import Admin
from models.user.role import Role

users = Blueprint("users",__name__, template_folder="views")

@users.route('/register_admin')
def register_admin():
    roles = Role.get_all_roles()



    return render_template("registerAdmin.html", roles = roles)

'''
@auth.route('/signup')
def signup():
    return render_template('registerUser.html')

@auth.route('/signup_client', methods=['POST'])
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

@auth.route('/signup_admin', methods=['POST'])
def signup_post_admin():
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
    
    print(new_user)
    user_id = new_user[object].id
    new_role = Role.create_role("operador")
    role_id = new_role["object"].id

    new_admin = Admin.create_admin(user_id, role_id)
    
    if not new_user["success"]:
        flash(", ".join(new_user["errors"]))
        return redirect(url_for('auth.signup'))

    return redirect(url_for('auth.login'))
'''
