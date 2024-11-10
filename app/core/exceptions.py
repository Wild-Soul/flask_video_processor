class VideoServiceException(Exception):
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
