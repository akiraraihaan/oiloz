"""
WSGI entry point for deployment (Gunicorn/Railway)
"""
from app import create_app, db
from app.utils import initialize_models

app = create_app()

# Initialize ML models on startup
with app.app_context():
    initialize_models()
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
