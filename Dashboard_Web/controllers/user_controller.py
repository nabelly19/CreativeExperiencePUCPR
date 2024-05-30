from flask import Blueprint, request, render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from models.user.users import Users
from models.user.client import Client
from models.user.admin import Admin
from models.user.role import Role


users = Blueprint("users",__name__, template_folder="views")

@users.route('/signup_admin')
def signup_admin():
    roles = Role.get_all_roles()

    return render_template("registerAdmin.html", roles = roles)

@users.route('/signup', methods=['POST'])
def signup_post_user():
    name = request.form.get('name')
    cpf = request.form.get('cpf')
    birth_date = request.form.get('birth_date')
    gender = request.form.get('gender')
    email = request.form.get('email')
    nickname = request.form.get('nickname')
    password = request.form.get('password')
    user_type = request.form.get('user_type')

    type = ['admin', 'client']

    user = Users.query.filter_by(email=email).first()

    if user:
        flash('Email address already exists')
        return redirect(url_for('users.signup'))

    new_user = Users.create_user(
        name=name, 
        cpf=cpf, 
        birth_date=birth_date,
        gender=gender, 
        email=email, 
        nickname=nickname, 
        password=generate_password_hash(password, method='pbkdf2:sha256'))
    
    user_id = new_user["object"].id
    
    #new_role = Role.create_role("operador")
    #role_id = new_role["object"].id
    #new_admin = Admin.create_admin(user_id, role_id)
    
    if not new_user["success"]:
        flash(", ".join(new_user["errors"]))
        return redirect(url_for('users.signup'))
    
    if user_type == type[0]:
        role = request.form.get('role')
        return redirect(url_for('users.signup_admin_2', user_id=user_id, role=role))
    # Criar rota de criação de admin e de client

    else:
        return "Deu ruim, não é adm nem client"

@users.route('/signup_admin2/<int:user_id>/<role>')
def signup_admin_2(user_id, role):

    

    # _,adm = Admin.create_admin(user_id, role_id)

    return render_template("teste.html", role = role)










@users.route('/signup_client')
def signup():
    return render_template('registerUser.html')

@users.route('/signup_client', methods=['POST'])
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
        return redirect(url_for('users.signup'))

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
        return redirect(url_for('users.signup'))

    return redirect(url_for('users.login'))