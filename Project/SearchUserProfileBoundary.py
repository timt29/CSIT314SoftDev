from flask import Blueprint, request, jsonify
from SearchUserProfileController import SearchUserProfileController

search_user_profile_bp = Blueprint("search_user_profile_bp", __name__)

@search_user_profile_bp.route("/api/user_profiles", methods=["GET"])
def search_user_profiles():
    search_query = request.args.get("search", "").strip()
    profiles = SearchUserProfileController.search_profiles(search_query)
    return jsonify(profiles)

def register_search_user_profile_routes(app):
    app.register_blueprint(search_user_profile_bp)
