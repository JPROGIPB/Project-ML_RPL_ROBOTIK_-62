from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO
from app.config import Config

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
socketio = SocketIO(cors_allowed_origins="*")


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app, origins=app.config['CORS_ORIGINS'])
    jwt.init_app(app)
    socketio.init_app(app)

    # Register blueprints
    from app.routes.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    from app.routes.robots import bp as robots_bp
    app.register_blueprint(robots_bp, url_prefix='/api/robots')

    from app.routes.products import bp as products_bp
    app.register_blueprint(products_bp, url_prefix='/api/products')

    from app.routes.bookings import bp as bookings_bp
    app.register_blueprint(bookings_bp, url_prefix='/api/bookings')

    from app.routes.certification import bp as cert_bp
    app.register_blueprint(cert_bp, url_prefix='/api/certification')

    from app.routes.dashboard import bp as dashboard_bp
    app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')

    # JWT error handlers for better debugging
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        print(f"[JWT] Token expired - Header: {jwt_header}, Payload: {jwt_payload}")
        return {'error': 'Token has expired', 'message': 'Please login again'}, 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        print(f"[JWT] Invalid token - Error: {error}")
        import traceback
        traceback.print_exc()
        return {'error': 'Invalid token', 'message': str(error)}, 422

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        print(f"[JWT] Missing token - Error: {error}")
        return {'error': 'Authorization required', 'message': 'Missing token in request'}, 401

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        print(f"[JWT] Token revoked - Header: {jwt_header}, Payload: {jwt_payload}")
        return {'error': 'Token has been revoked', 'message': 'Please login again'}, 401

    return app

