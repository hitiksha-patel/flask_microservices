from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# Initialize the database
db = SQLAlchemy()

def create_app():
    # Load environment variables from .env file
    load_dotenv()

    app = Flask(__name__)

    # Load configurations from environment variables
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the database with the app
    db.init_app(app)

    with app.app_context():
        # Import routes (or other components that need the app context)
        from . import routes

    return app
