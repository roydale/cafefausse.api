from app.routes.reservation_routes import reservation_bp

API_PREFIX = '/api'

def register_blueprints(app):
    app.register_blueprint(reservation_bp, url_prefix=combine_prefix(reservation_bp.url_prefix))

def combine_prefix(bp_prefix):
    """Safely concatenate two URL prefixes without duplicate slashes."""
    return f'{API_PREFIX.rstrip("/")}/{bp_prefix.lstrip("/")}'