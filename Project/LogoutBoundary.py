from flask import redirect
from LogoutController import LogoutController

def register_routes(app):

    @app.route("/logout", methods=["GET"])
    def logout_route():
        return LogoutController.logout()
