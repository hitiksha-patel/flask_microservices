from flask import current_app as app
from . import db
from . models import User
from sqlalchemy import text
from flask import request, jsonify

@app.route('/')
def index():
    return "Hello, Flask Microservice!"

@app.route('/db_check')
def db_check():
    try:
        with db.engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            return "Database Connected!"
    except Exception as e:
        return f"Database Connection Failed: {str(e)}"


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Validate that required fields are present
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Missing required fields'}), 400

    # Check if user already exists
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'User with this email is already exists'}), 400

    try:
        # Create a new user
        new_user = User(email=email)
        new_user.set_password(password)  # Hash the password before storing it
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()  # Roll back the session in case of error
        return jsonify({'error': str(e)}), 500

    return jsonify({'message': 'User registered successfully'}), 201


