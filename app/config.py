class Config:
    # Video configurations
    MAX_FILE_SIZE_MB = 25
    MIN_VIDEO_DURATION = 5 # seconds
    MAX_VIDEO_DURATION = 300 # seconds
    ALLOWED_VIDEOS_MIME_TYPE = ['video/mp4', ['video/quicktime']]

    # DB configurations
    SQLALCHEMY_DATABASE_URI = 'sqlite:///videos.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Minio configurations

