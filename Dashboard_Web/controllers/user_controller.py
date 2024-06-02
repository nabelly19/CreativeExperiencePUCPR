# In this file it will be doing the CRUD of the user (admin, clients and root)

from flask import Blueprint, request, render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from controllers.auth_controller import roles_required
from flask_login import login_required
from models.user.users import Users
from models.user.role import Role
from models.user.client import Client
from models.user.admin import Admin


#setting up the blueprint
users = Blueprint("users",__name__, template_folder="views")

#Create part of the user
#general route to create an user, later on, we'll be creating either an admin or a client
@users.route('/signup', methods=['POST'])
@login_required
@roles_required('Root')
def signup_post_user():
    name = request.form.get('name')
    cpf = request.form.get('cpf')
    birth_date = request.form.get('birth_date')
    email = request.form.get('email')
    nickname = request.form.get('nickname')
    password = request.form.get('password')
    user_type = request.form.get('user_type')

    type = ['admin', 'client']

    exists_email = Users.query.filter_by(email=email).first()
    exists_cpf = Users.query.filter_by(cpf=cpf).first()
    exists_nickname = Users.query.filter_by(nickname=nickname).first()

    if exists_email or exists_cpf or exists_nickname:
        # flash('Email address already exists')
        flash('Esse usuário já está cadastrado!')
        
        if user_type == type[0]: # Caso seja cadastro de adm
            return redirect(url_for('users.signup_admin'))
        if user_type == type[1]: # Caso seja cadastro de client
            return redirect(url_for('users.signup_client'))

    new_user = Users.create_user(
        name=name, 
        cpf=cpf, 
        birth_date=birth_date,
        email=email, 
        nickname=nickname, 
        password=generate_password_hash(password, method='pbkdf2:sha256'))
    
    user_id = new_user["object"].id
    
    if not new_user["success"]:
        flash(", ".join(new_user["errors"]))
        return redirect(url_for('users.signup'))
    
    # in case it is creating a new admin. Also requests it's role.
    if user_type == type[0]:
        role_id = request.form.get('role')
        return redirect(url_for('users.add_admin', user_id=user_id, role_id=role_id))
    
    # in case it is creating a new client 
    elif user_type == type[1]:
        return redirect(url_for('users.add_client', user_id=user_id))

    # exception treatment
    else:
        return flash("Ops! Something went wrong.")

@users.route('/signup_client')
@login_required
@roles_required('Root')
def signup_client():
    return render_template("registerClient.html")

#route to create the new client
@users.route('/add_client/<int:user_id>')
@login_required
@roles_required('Root')
def add_client(user_id):
    # creating the client
    new_client = Client.create_client(user_id)

    # tests if the new_client dictionary has a 'success' message on it
    if not new_client["success"]:
        flash(", ".join(new_client["errors"]))
        return redirect(url_for('users.signup'))
    
    # return render_template("teste.html", user_id = user_id)
    return redirect(url_for('users.users_list'))
    
    #routes to create an admin
@users.route('/signup_admin')
@login_required
@roles_required('Root')
def signup_admin():
    roles = Role.get_all_roles()
    return render_template("registerAdmin.html", roles = roles)

#note that we're using two routes two create an admin, while creating a client, only one. The need on using two resids in the necessity to get the roles displayed in the screen.
@users.route('/add_admin/<int:user_id>/<string:role_id>')
@login_required
@roles_required('Root')
def add_admin(user_id, role_id):

    new_adm = Admin.create_admin(user_id, role_id)

    if not new_adm["success"]:
        flash(", ".join(new_adm["errors"]))
        return redirect(url_for('users.signup'))

    return redirect(url_for('auth.login'))

#route to list the users after creating one
@users.route('/users/list')
@login_required
@roles_required('Root')
def users_list():
    #clients = Client.get_clients_with_users()
    users = Users.get_users_with_admin_client()
    admins = Admin.get_all_admins()

    if not users:
        flash('Sem registros no momentos!')

    return render_template("userList.html", admins=admins, users=users)


#the Update part of the user
@users.route('/renovate_user', methods=['POST'])
@login_required
@roles_required('Root')
def renovate_user():
    id = request.args.get('id', None)
    name = request.form.get("user_name")
    nickname = request.form.get("user_nickname")
    email = request.form.get("user_email")
    cpf = request.form.get("user_cpf")
    birth_date = request.form.get("user_birth_date")
    is_active = True if request.form.get("is_active") == "on" else False
    # password = request.form.get("topic_title")

    update_user = Users.update_user(id, name, email, nickname, is_active, cpf, birth_date)

    if not update_user["success"]:
        flash(", ".join(update_user["errors"]))
    
    return redirect(url_for('users.users_list'))

#the Delete part of the user
@users.route('/del_user')
@login_required
@roles_required('Root')
def del_user():
    id = request.args.get('id', None)
    Users.delete_user(id)

    return redirect(url_for('users.users_list'))