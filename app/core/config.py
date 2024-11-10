import os

class Config:
    # For development only, should be set to false in production env.
    DEBUG = os.getenv('DEBUG', True)
    TESTING = os.getenv('TESTING', False)
    
    SQLITE_PATH = os.getenv('SQLITE_PATH', 'video_service.db')

    # Hard coded token for authz
    API_TOKEN_HEADER = 'Authorization'
    API_TOKEN_PREFIX = 'Bearer'
    VALID_API_TOKENS = os.getenv('VALID_API_TOKENS', 'test-token').split(',')

    # Video configurations
    MAX_FILE_SIZE_MB = 25
    MIN_VIDEO_DURATION = 5 # seconds
    MAX_VIDEO_DURATION = 300 # seconds
    ALLOWED_VIDEOS_MIME_TYPE = ['video/mp4', 'video/quicktime']

    # DB configurations
    SQLALCHEMY_DATABASE_URI = 'sqlite:///videos.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # MinIO Configuration
    MINIO_ENDPOINT = os.getenv('MINIO_ENDPOINT', 'localhost:9090')
    MINIO_ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY', 'minioadmin')
    MINIO_SECRET_KEY = os.getenv('MINIO_SECRET_KEY', 'minioadmin')
    MINIO_BUCKET = os.getenv('MINIO_BUCKET', 'videos')

