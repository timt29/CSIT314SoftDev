from flask import request, jsonify
from CreateUserProfileController import CreateUserProfileController
from UpdateUserProfileController import UpdateUserProfileController
from DeleteUserProfileController import DeleteUserProfileController
from SearchUserProfileController import SearchUserProfileController
from UserProfile import UserProfile  # Entity for view

def register_profile_routes(app):

    # Create user profile
    @app.route("/api/user_profiles", methods=["POST"])
    def create_profile():
        data = request.json
        role = data.get("role")
        description = data.get("description")

        if not role or not description:
            return jsonify({"error": "Missing role or description"}), 400

        result, status = CreateUserProfileController.create_profile(role, description)
        return jsonify(result), status

    # View all user profiles (with optional search)
    @app.route("/api/user_profiles", methods=["GET"])
    def get_user_profiles():
        search_query = request.args.get("search")
        profiles = UserProfile.get_user_profiles(search_query)
        return jsonify([
            {"Role": p["Role"], "Description": p["Description"]}
            for p in profiles
        ])

    # Update user profile
    @app.route("/api/user_profiles/<string:role>", methods=["PUT"])
    def update_profile(role):
        data = request.json
        description = data.get("description")

        if not description:
            return jsonify({"error": "Missing description"}), 400

        result, status = UpdateUserProfileController.update_description(role, description)
        return jsonify(result), status

    # Delete user profile
    @app.route("/api/user_profiles/<string:role>", methods=["DELETE"])
    def delete_user_profile(role):
        result = DeleteUserProfileController.delete_profile(role)
        return jsonify(result[0]), result[1]

    # Search profiles (alternate path)
    @app.route("/api/user_profiles/search", methods=["GET"])
    def search_user_profiles():
        search_query = request.args.get("search", "").strip()
        profiles = SearchUserProfileController.search_profiles(search_query)
        return jsonify(profiles)
