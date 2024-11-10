class VideoServiceException(Exception):
    """Base exception for any video related operation."""
    def __init__(self, message: str, code: int = 500):
        self.message = message
        self.code = code
        super().__init__(message)

class ValidationError(VideoServiceException):
    def __init__(self, message: str):
        super().__init__(message, 400)

class AuthenticationError(VideoServiceException):
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, 401)


class VideoAPIException(Exception):
    """Base exception for API based exception, like storage related"""
    def __init__(self, message, status_code=500):
        super().__init__(message)
        self.status_code = status_code

class VideoProcessingError(VideoAPIException):
    """Raised when video processing fails"""
    pass

class StorageError(VideoAPIException):
    """Raised when storage operations fail"""
    pass
