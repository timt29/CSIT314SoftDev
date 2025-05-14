from flask import request, render_template, redirect, url_for, session, jsonify
from ViewServiceController import ViewServiceController

def register_routes(app):

    @app.route("/dashboard_cleaner")
    def cleaner_dashboard():
        user = session.get("user")
        print("Session Data:", user)

        if not user:
            return redirect(("/"))

        cleaner_name = user.get("Name")
        user_id = user.get("UserId")

        services = ViewServiceController.get_service(user_id)

        return render_template("dashboard_cleaner.html", cleaner_name=cleaner_name, services=services)

    @app.route("/get_cleaner_services", methods=["GET"])
    def get_cleaner_services():
        user = session.get("user")
        user_id = user.get("UserId") if user else None
        if not user_id:
            return jsonify({"error": "User not logged in"}), 401

        services = ViewServiceController.get_service(user_id)
        return jsonify(services)
    

        