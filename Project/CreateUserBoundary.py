from flask import render_template, request, redirect, url_for, flash, jsonify
from CreateUserController import CreateUserController

def register_create_user_routes(app):
    from flask import request, jsonify
    @app.route('/api/users', methods=['POST'])
    def api_create_user():
        data = request.get_json()
        if not data:
            return jsonify({"message": "No input data provided"}), 400

        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role')
        dob = data.get('dob')
        status = data.get('status', 'Active')

    # Check for missing fields
        if not all([name, email, password, role, dob]):
            return jsonify({"message": "Missing required fields"}), 400

    # Call your controller (argument order must match your User.create_user)
        success, message = CreateUserController.create_user(email, name, password, role, dob, status)
        if success:
            return jsonify({"message": "User created successfully."}), 201
        else:
            return jsonify({"message": message}), 400