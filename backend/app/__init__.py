from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_login import LoginManager
from config import Config
import os

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app, origins=['http://localhost:3000'], supports_credentials=True)
    login_manager.init_app(app)
    
    # Create upload directory if it doesn't exist
    upload_dir = os.path.join(app.instance_path, '..', 'static', 'uploads')
    os.makedirs(upload_dir, exist_ok=True)
    
    # Register blueprints
    from app.routes.auth import bp as auth_bp
    from app.routes.menus import bp as menus_bp
    from app.routes.orders import bp as orders_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(menus_bp)
    app.register_blueprint(orders_bp)
    
    # Import models to register them with SQLAlchemy
    from app.models import admin, menu, order
    
    return app

@login_manager.user_loader
def load_user(user_id):
    from app.models.admin import Admin
    return Admin.query.get(int(user_id))