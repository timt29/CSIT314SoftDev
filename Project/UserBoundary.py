from flask import request, render_template, redirect, url_for, flash, jsonify, session
from CreateUserController import CreateUserController
from ViewUserController import ViewUserController
from UpdateUserController import UpdateUserController
from SuspendUserController import SuspendUserController
from SearchController import SearchController

def register_user_routes(app):

    # Dashboard view
    @app.route("/dashboard_admin")
    def admin_dashboard():
        return render_template("dashboard_admin.html")

    # Create user
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

        if not all([name, email, password, role, dob]):
            return jsonify({"message": "Missing required fields"}), 400

        success, message = CreateUserController.create_user(email, name, password, role, dob, status)
        if success:
            return jsonify({"message": "User created successfully."}), 201
        else:
            return jsonify({"message": message}), 400

    # Get all users (with optional name/email filters)
    @app.route("/api/users", methods=["GET"])
    def get_users():
        name = request.args.get("name")
        email = request.args.get("email")
        users = ViewUserController.get_users(name=name, email=email)  
        return jsonify(users)

    # Update user
    @app.route("/api/users/<string:email>", methods=["PUT"])
    def update_user(email):
        data = request.json
        new_email = data.get("new_email")
        name = data.get("name")
        role = data.get("role")

        result = UpdateUserController.update_user(email, new_email, name, role)
        return jsonify(result)

    # Suspend user
    @app.route("/api/users/<string:email>/suspend", methods=["PATCH"])
    def suspend_user(email):
        result = SuspendUserController.suspend_user(email)
        return jsonify(result)

    # Search users
    @app.route("/users", methods=["GET"])
    def search_users():
        search_query = request.args.get("search", "").strip()
        users = SearchController.search_users(search_query)
        return jsonify(users)
