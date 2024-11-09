"""
Prefer to run with Gunicorn in production.

Example usage with Gunicorn:
    gunicorn wsgi:app --workers=3 --bind=0.0.0.0:8000
"""
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
