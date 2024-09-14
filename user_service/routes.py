from flask import current_app as app
from user_service import db
from user_service.models import User
from sqlalchemy import text

@app.route('/')
def index():
    return "Hello, Flask Microserviceeee!"

@app.route('/create_user')
def create_user():
    user = User(username="test_user", email="test@example.com")
    db.session.add(user)
    db.session.commit()
    return "User created!"

@app.route('/db_check')
def db_check():
    print("checking database...")
    try:
        # Use a raw SQL statement with the newer SQLAlchemy API
        with db.engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            return "Database Connected!"
    except Exception as e:
        return f"Database Connection Failed: {str(e)}"
