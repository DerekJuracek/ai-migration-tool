from flask import Blueprint
import os

chat_bp = Blueprint('chat', __name__, url_prefix='/chat')

from migration_app.chat import routes
