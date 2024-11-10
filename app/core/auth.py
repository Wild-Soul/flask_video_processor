from functools import wraps
from flask import request, current_app
from .exceptions import AuthenticationError

def validate_token(token: str) -> bool:
    """Validate API token against configured tokens"""
    valid_tokens = current_app.config['VALID_API_TOKENS']
    return token in valid_tokens

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            raise AuthenticationError("No authorization header")
        
        try:
            scheme, token = auth_header.split()
            if scheme.lower() != 'bearer':
                raise AuthenticationError("Invalid authentication scheme")
            if not validate_token(token):
                raise AuthenticationError("Invalid token")
        except ValueError:
            raise AuthenticationError("Invalid authorization header format")
        
        return f(*args, **kwargs)
    return decorated
