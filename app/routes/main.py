from flask import Blueprint, render_template, send_from_directory, current_app

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/submit.html')
def submit():
    return render_template('submit.html')

@bp.route('/track.html')
def track():
    return render_template('track.html')

@bp.route('/login.html')
def login_page():
    return render_template('login.html')

@bp.route('/signup.html')
def signup_page():
    return render_template('signup.html')

@bp.route('/my_complaints.html')
def my_complaints_page():
    return render_template('my_complaints.html')

@bp.route('/admin_login.html')
def admin_login_page():
    return render_template('admin_login.html')

@bp.route('/admin_dashboard.html')
def admin_dashboard():
    return render_template('admin_dashboard.html')
