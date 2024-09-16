from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from .models import User
from . import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    # Find user by email
    user = User.query.filter_by(email=email).first()

    # Verify password
    if not user or not user.check_password(password):
        return jsonify({'message': 'Invalid email or password'}), 401

    # Generate JWT token
    access_token = create_access_token(identity=user.id)
    return jsonify({'access_token': access_token}), 200

@auth_bp.route('/change_password', methods=['POST'])
@jwt_required()
def change_password():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    data = request.json
    new_password = data.get('new_password')

    if not new_password:
        return jsonify({'message': 'Missing new password'}), 400

    # Set the new password
    user.set_password(new_password)
    db.session.commit()

    return jsonify({'message': 'Password changed successfully!'}), 200
