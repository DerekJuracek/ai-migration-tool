from flask import Blueprint
import os

home_bp = Blueprint('home', __name__)

from migration_app.home import routes