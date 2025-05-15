from flask import Blueprint, jsonify
from DeleteUserProfileController import DeleteUserProfileController

delete_user_profile_bp = Blueprint("delete_user_profile_bp", __name__)

@delete_user_profile_bp.route("/api/user_profiles/<string:role>", methods=["DELETE"])
def delete_user_profile(role):
    result = DeleteUserProfileController.delete_profile(role)
    return jsonify(result[0]), result[1]

def register_delete_user_profile_routes(app):
    app.register_blueprint(delete_user_profile_bp)
