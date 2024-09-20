from flask import Blueprint, current_app as app
from flask_jwt_extended import create_access_token
from . import db
from . models import User
from sqlalchemy import text
from flask import request, jsonify

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/')
def index():
    return "Hello, Flask Microservice!"

@user_blueprint.route('/db_check', methods=['GET'])
def db_check():
    try:
        with db.engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            return "Database Connected!"
    except Exception as e:
        return f"Database Connection Failed: {str(e)}"


@user_blueprint.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Missing required fields'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'User with this email already exists'}), 409

    try:
        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

    return jsonify({'message': 'User registered successfully'}), 201


@user_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    user = User.query.filter_by(email=email).first()

    if user is None or not user.verify_password(password):
        return jsonify({'error': 'Invalid email or password'}), 401

    access_token = create_access_token(identity=user.email)

    return jsonify({'token': access_token}), 200


