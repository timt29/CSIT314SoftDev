from flask import jsonify
from SuspendUserController import SuspendUserController

def register_routes(app):

    @app.route("/api/users/<string:email>/suspend", methods=["PATCH"])
    def suspend_user(email):
        result = SuspendUserController.suspend_user(email)
        return jsonify(result)
