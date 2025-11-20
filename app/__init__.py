from flask import Flask
from flask_cors import CORS
from config import Config
from app.db import close_db, init_db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    CORS(app)
    
    # Register database teardown context
    app.teardown_appcontext(close_db)
    
    # Initialize DB
    init_db(app)
    
    # Register Blueprints
    from app.routes.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    from app.routes.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api')
    
    from app.routes.complaints import bp as complaints_bp
    app.register_blueprint(complaints_bp, url_prefix='/api')
    
    from app.routes.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/api/admin')

    return app
