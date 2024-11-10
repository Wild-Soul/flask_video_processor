from flask import Flask
from flask_cors import CORS
from app.core.config import Config
from .extensions import db
from .api.v1.routes import bp_v1
from .factories import ServiceFactory

def create_app(config_class=Config):
    app = Flask(__name__)
    
    app.config.from_object(config_class)
    CORS(app)
    db.init_app(app)

    
    with app.app_context():
        # Initialize services needed for this app in one place.
        ServiceFactory.create_services(app)
        # Ensure all tables are created
        db.create_all()
    
    # Register blueprints
    app.register_blueprint(bp_v1)
    
    return app
