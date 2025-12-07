from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from models import db, bcrypt

def create_app(config_class=Config):
    """Application factory"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt = JWTManager(app)
    CORS(app, origins=app.config['CORS_ORIGINS'])
    
    # Register blueprints
    from routes.auth import auth_bp
    from routes.devices import devices_bp
    from routes.monitoring import monitoring_bp
    from routes.analysis import analysis_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(devices_bp, url_prefix='/api/devices')
    app.register_blueprint(monitoring_bp, url_prefix='/api/monitoring')
    app.register_blueprint(analysis_bp, url_prefix='/api/analysis')
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    # Health check endpoint
    @app.route('/api/health')
    def health():
        return jsonify({'status': 'healthy'}), 200
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app


if __name__ == '__main__':
    app = create_app()
    print("Starting Flask server on http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
