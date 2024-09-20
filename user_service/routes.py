from flask import Blueprint, current_app as app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
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

@user_blueprint.route('/update_user', methods=['PUT'])
@jwt_required()
def update_user():
    try:
        print("Entering update_user route")
        current_user_email = get_jwt_identity()
        print(f"Current user email: {current_user_email}")

        # Fetch the current user from the database
        user = User.query.filter_by(email=current_user_email).first()
        if user is None:
            return jsonify({"error": "User not found"}), 404

        # Get form fields from request
        print("Getting form data")
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        phone = request.form.get('phone')
        address = request.form.get('address')

        # Check if a profile picture file is uploaded
        profilepic = request.files.get('profilepic', None)
        if profilepic:
            print(f"Received file: {profilepic.filename}")
            profilepic.save(f'./uploads/{profilepic.filename}')
            user.profilepic = profilepic.filename

        if firstname:
            user.firstname = firstname
        if lastname:
            user.lastname = lastname
        if phone:
            user.phone = phone
        if address:
            user.address = address

        print("Committing changes to database")
        db.session.commit()
        return jsonify({'message': 'User details updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error occurred: {str(e)}")
        return jsonify({'error': str(e)}), 500
