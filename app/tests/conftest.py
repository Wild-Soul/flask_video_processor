import pytest
from app import create_app
from app.extensions import db
from app.factories import ServiceFactory
from unittest.mock import MagicMock
from flask import Flask

# Test Configuration for Flask App
class TestConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # In-memory SQLite for testing
    TESTING = True
    MINIO_ENDPOINT = 'localhost:9000'
    MINIO_ACCESS_KEY = 'minioadmin'
    MINIO_SECRET_KEY = 'minioadmin'
    MINIO_BUCKET_NAME = 'test-bucket'
    VALID_API_TOKENS = 'test-token'


@pytest.fixture
def valid_auth_header():
    """Fixture to provide a valid Authorization header."""
    # Assuming a mock JWT token
    return {
        'Authorization': 'Bearer test-token'
    }

@pytest.fixture(scope='module')
def app() -> Flask:
    """Create and configure a new Flask app instance for testing."""
    app = create_app(config_class=TestConfig)
    yield app


@pytest.fixture(scope='module')
def client(app):
    """Create a test client for making requests to the app."""
    return app.test_client()


@pytest.fixture(scope='module')
def init_db(app):
    """Initialize the database for tests (run once for all tests)."""
    with app.app_context():
        db.create_all()
        yield db
        db.drop_all()


# Mock MinIO Service
@pytest.fixture(scope='function')
def mock_minio(mocker):
    """Mock the MinIO interactions in the video service."""
    mock_minio_service = MagicMock()
    
    # Mock video upload function in MinIO service
    mock_minio_service.upload_video.return_value = {'success': True, 'data': {'video_id': '1234'}}
    
    # Replace the actual MinIO service with the mocked one
    mocker.patch.object(ServiceFactory, 'get_service', return_value=mock_minio_service)
    
    return mock_minio_service
