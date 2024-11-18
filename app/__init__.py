from flask import Flask, jsonify
from flask_cors import CORS
from flask_apispec.extension import FlaskApiSpec
from werkzeug.exceptions import HTTPException

from app.core.config import Config
from app.core.exceptions import VideoAPIException, VideoServiceException
from .extensions import db
from .api.v1.routes import bp_v1, register_docs
from .factories import ServiceFactory

def create_app(config_class=Config):
    app = Flask(__name__)
    
    app.config.from_object(config_class)
    CORS(app)
    db.init_app(app)
    
    # Global error handler
    @app.errorhandler(HTTPException)
    def handle_http_exception(error: HTTPException):
        response = {
            'message': error.description,
            'status_code': error.code
        }
        return jsonify(response), error.code
    
    @app.errorhandler(VideoServiceException)
    def handle_video_service_exception(error: VideoServiceException):
        # Custom error handler for validation errors
        response = {
            'message': error.message,
            'status_code': error.code
        }
        return jsonify(response), error.code

    @app.errorhandler(VideoAPIException)
    def handle_video_processing_exceptions(error: VideoAPIException):
        response = {
            "code": error.status_code,
            "message": error.message
        }
    @app.errorhandler(Exception)
    def handle_generic_exception(error):
        # Catch any unexpected errors
        response = {
            'message': 'Internal server error',
            'error': str(error),
            'status_code': 500
        }
        return jsonify(response), 500

    with app.app_context():
        # Initialize services needed for this app in one place.
        ServiceFactory.create_services(app)
        # Ensure all tables are created
        db.create_all()
        # Register blueprints
        app.register_blueprint(bp_v1)
        # Create swagger docs
        docs = FlaskApiSpec(app)
        register_docs(docs)    
    
    return app
