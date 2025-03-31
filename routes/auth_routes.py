from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token
from models import User
from db import db

auth_routes = Blueprint('auth_routes', __name__)

@auth_routes.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Validation: Check required fields
    for field in ['username', 'email', 'password']:
        if not data.get(field):
            return jsonify({"error": f"{field} is required"}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email already registered"}), 400

    # Hash the password using bcrypt from app context
    hashed_password = current_app.extensions['bcrypt'].generate_password_hash(data['password']).decode('utf-8')

    user = User(username=data['username'], email=data['email'], password_hash=hashed_password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

@auth_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    # Validation: Check required fields
    for field in ['email', 'password']:
        if not data.get(field):
            return jsonify({"error": f"{field} is required"}), 400

    user = User.query.filter_by(email=data['email']).first()

    bcrypt = current_app.extensions['bcrypt']

    if user and bcrypt.check_password_hash(user.password_hash, data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200

    return jsonify({"error": "Invalid credentials"}), 401
