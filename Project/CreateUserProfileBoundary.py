from flask import Blueprint, request, jsonify
from CreateUserProfileController import CreateUserProfileController

create_profile_bp = Blueprint("create_profile_bp", __name__)

@create_profile_bp.route("/api/user_profiles", methods=["POST"])
def create_profile():
    data = request.json
    role = data.get("role")
    description = data.get("description")

    if not role or not description:
        return jsonify({"error": "Missing role or description"}), 400

    result, status = CreateUserProfileController.create_profile(role, description)
    return jsonify(result), status

def register_create_profile_routes(app):
    app.register_blueprint(create_profile_bp)
