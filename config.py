import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Use /tmp for cloud platforms (writable directory)
    if os.environ.get('RENDER') or os.environ.get('RAILWAY_ENVIRONMENT'):
        DB_PATH = '/tmp/complaint_box.db'
    else:
        DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'complaint_box.db')
    
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
