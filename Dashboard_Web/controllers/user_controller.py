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


