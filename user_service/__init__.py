from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

# Initialize the database
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    # Load environment variables from .env file
    load_dotenv()

    app = Flask(__name__)

    # Load configurations from environment variables
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the database with the app
    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        # Import routes (or other components that need the app context)
        from .models import User

        db.create_all()

    return app
