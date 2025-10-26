from flask import Flask
from flask_migrate import Migrate
from app.routes import register_blueprints
from .extensions import db, cors, migrate
from .config import Config
from .seed_data import seed_data
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)    
    migrate.init_app(app, db)
    
    # Enable CORS
    cors.init_app(app, resources={r"/*": {"origins": app.config['CORS_ORIGINS']}})

    # Import models so Alembic and SQLAlchemy can detect them
    from app import models

    # Register blueprints
    register_blueprints(app)
    
    # Create tables and seed data
    with app.app_context():
        db.create_all()
        seed_data()

    return app