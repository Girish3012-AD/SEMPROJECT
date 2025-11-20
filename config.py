import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'complaint_box.db')
    DEBUG = True
