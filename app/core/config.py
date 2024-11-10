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
    MAX_VIDEO_SIZE = 25 * 1024 * 1024 # in bytes
    MIN_VIDEO_DURATION = 5 # seconds
    MAX_VIDEO_DURATION = 300 # seconds
    ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'webm', 'mov', 'avi'}
    EXTENSION_CODE_MAP = {
        'mp4': 'libx264',
        'webm': 'libvpx',
        'avi': 'libxvid',
        'mov': 'prores',
    }

    # DB configurations
    SQLALCHEMY_DATABASE_URI = 'sqlite:///videos.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # MinIO Configuration
    MINIO_ENDPOINT = os.getenv('MINIO_ENDPOINT', 'localhost:9000')
    MINIO_ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY', 'minioadmin')
    MINIO_SECRET_KEY = os.getenv('MINIO_SECRET_KEY', 'minioadmin')
    MINIO_BUCKET_NAME = os.getenv('MINIO_BUCKET_NAME', 'videos')

    # Share expiry default
    DEFAULT_SHARE_EXPIRY = 10 # 10 mins
    