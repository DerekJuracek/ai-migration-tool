from flask import render_template, current_app
from migration_app.home import home_bp as home

@home.route('/home')
@home.route('/')
def index():
    return render_template('home.html')