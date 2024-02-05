from flask import Flask
from key import get_flask_secret_key

import os


app = Flask(__name__)

def create_app():
    app.secret_key =  get_flask_secret_key()
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'uploads')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit
    # RQ Configuration
    app.config['RQ_REDIS_URL'] = 'redis://redis:6379/0'# Add app configuration and other setup here if needed.
    return app
