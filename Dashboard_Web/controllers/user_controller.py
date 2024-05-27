from flask import Blueprint, request, render_template, redirect, url_for, flash
from models.user.users import Users
from models.user.client import Client
from models.user.admin import Admin

users = Blueprint("users",__name__, template_folder="views")

