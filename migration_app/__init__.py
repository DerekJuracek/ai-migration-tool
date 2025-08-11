from flask import Flask
from dotenv import load_dotenv
import os
from flask import Flask, Blueprint, render_template, session
from migration_app.home import home_bp
from migration_app.chat import chat_bp

load_dotenv() 

def create_app():
    app = Flask(__name__, instance_relative_config=True )
    migration_app = Blueprint('migration_app', __name__, url_prefix="/migration", static_folder='static', template_folder='templates')
    migration_app.register_blueprint(home_bp)
    migration_app.register_blueprint(chat_bp)
    app.register_blueprint(migration_app)
    app.config['OPENAI_KEY'] = os.environ.get('OPEN_AI_KEY')
    app.secret_key = 'top-secret'
    
   
    @app.route('/')
    def index():
        return render_template('home.html')
    return app
