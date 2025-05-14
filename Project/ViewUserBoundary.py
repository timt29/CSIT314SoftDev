from flask import request, render_template, redirect, url_for, session, jsonify
from ViewUserController import ViewUserController

def register_routes(app):

    @app.route("/dashboard_admin")
    def admin_dashboard():
        return render_template("dashboard_admin.html")

    @app.route("/api/users", methods=["GET"])
    def get_users():
        name = request.args.get("name")
        email = request.args.get("email")
        users = ViewUserController.get_users(name=name, email=email)  
        return jsonify(users)