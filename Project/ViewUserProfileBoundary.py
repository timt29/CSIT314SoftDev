from flask import jsonify, request, Blueprint
from UserProfile import UserProfile

view_user_profile_blueprint = Blueprint('view_user_profile', __name__)

@view_user_profile_blueprint.route("/api/user_profiles", methods=["GET"])
def get_user_profiles():
    search_query = request.args.get("search")
    profiles = UserProfile.get_user_profiles(search_query)
    # Ensure keys match your JS: Role and Description
    return jsonify([
        {"Role": p["Role"], "Description": p["Description"]}
        for p in profiles
    ])

def register_view_user_profile_routes(app):
    app.register_blueprint(view_user_profile_blueprint)