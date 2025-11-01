from flask import Flask
from flask_migrate import Migrate
from app.routes import register_blueprints
from .extensions import db, cors, migrate
from .config import Config
from .seed_data import seed_data
migrate = Migrate()
from flask.cli import with_appcontext
import click

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
    
    # Register commands
    register_commands(app)
    
    # Create tables
    with app.app_context():
        db.create_all()

    return app

@click.command(name='seed')
@with_appcontext
def seed_command():
    """Seed initial data into the database."""
    from .seed_data import seed_data
    seed_data()
    click.echo('Database seeded successfully.')

def register_commands(app):
    app.cli.add_command(seed_command)