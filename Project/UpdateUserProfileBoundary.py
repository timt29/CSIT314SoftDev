from flask import Blueprint, request, jsonify
from UpdateUserProfileController import UpdateUserProfileController

update_profile_bp = Blueprint("update_profile_bp", __name__)

@update_profile_bp.route("/api/user_profiles/<string:role>", methods=["PUT"])
def update_profile(role):
    data = request.json
    description = data.get("description")

    if not description:
        return jsonify({"error": "Missing description"}), 400

    result, status = UpdateUserProfileController.update_description(role, description)
    return jsonify(result), status

def register_update_profile_routes(app):
    app.register_blueprint(update_profile_bp)
