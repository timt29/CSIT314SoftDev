from flask import Blueprint, request, jsonify
from UpdateUserController import UpdateUserController

update_user_bp = Blueprint("update_user_bp", __name__)

@update_user_bp.route("/api/users/<string:email>", methods=["PUT"])
def update_user(email):
    data = request.json
    new_email = data.get("new_email")
    name = data.get("name")
    role = data.get("role")

    result = UpdateUserController.update_user(email, new_email, name, role)
    return jsonify(result)

def register_update_user_routes(app):
    app.register_blueprint(update_user_bp)
