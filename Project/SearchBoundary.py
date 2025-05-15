from flask import Blueprint, request, jsonify
from SearchController import SearchController

search_bp = Blueprint("search_bp", __name__)

@search_bp.route("/users", methods=["GET"])
def search_users():
    search_query = request.args.get("search", "").strip()
    users = SearchController.search_users(search_query)
    return jsonify(users)

def register_search_routes(app):
    app.register_blueprint(search_bp)
