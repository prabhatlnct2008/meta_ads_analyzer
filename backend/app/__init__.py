import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

from app.database import init_db

# Load environment variables
load_dotenv()

def create_app():
    """Create and configure Flask app"""
    app = Flask(__name__)

    # Configuration
    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///meta_ads_analyzer.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }

    # Enable CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": os.getenv('FRONTEND_URL', 'http://localhost:3000'),
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })

    # Initialize database
    init_db(app)

    # Import and register blueprints
    from app.routes.auth import auth_bp
    from app.routes.meta import meta_bp
    from app.routes.analytics import analytics_bp
    from app.routes.chat import chat_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(meta_bp, url_prefix='/api/meta')
    app.register_blueprint(analytics_bp, url_prefix='/api/analytics')
    app.register_blueprint(chat_bp, url_prefix='/api/chat')

    # Health check endpoint
    @app.route('/health')
    def health():
        return {'status': 'healthy', 'message': 'Meta Ads Analyzer API is running'}

    return app
