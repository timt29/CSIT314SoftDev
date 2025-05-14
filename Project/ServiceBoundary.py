from flask import request, render_template, redirect, url_for, session, jsonify
from ViewServiceController import ViewServiceController
from CreateServiceController import CreateServiceController
from UpdateServiceController import UpdateServiceController
from DeleteServiceController import DeleteServiceController
from SearchServiceController import SearchServiceController

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
    
    @app.route("/api/cleaner/services", methods=["POST"])
    def add_service():
        user = session.get("user")
        user_id = user.get("UserId") 
        if not user:
            return jsonify({"error": "Not logged in"}), 401

        data = request.json
        name = data.get("name")
        price = data.get("price")
        duration = data.get("duration")

        if not all([name, price, duration]):
            return jsonify({"error": "Missing required fields"}), 400

        response, status = CreateServiceController.add_service(
            user_id, name, price, duration
        )
        return jsonify(response), status
    
    @app.route("/api/cleaner/services/<int:service_id>", methods=["PUT"])
    def update_service(service_id):
        user = session.get("user")
        if not user:
            return jsonify({"error": "Not logged in"}), 401

        data = request.json
        name = data.get("name")
        price = data.get("price")
        duration = data.get("duration")

        if not all([name, price, duration]):
            return jsonify({"error": "Missing fields"}), 400

        response, status = UpdateServiceController.update_service(
            service_id, name, price, duration
        )
        return jsonify(response), status
    
    @app.route("/api/cleaner/services/<int:service_id>", methods=["DELETE"])
    def delete_service(service_id):
        user = session.get("user")
        if not user:
            return jsonify({"error": "Not logged in"}), 401

        response, status = DeleteServiceController.delete_service(service_id)
        return jsonify(response), status
    
    @app.route("/api/cleaner/search_service", methods=["GET"])
    def search_service():
        user = session.get("user")
        if not user:
            return jsonify({"error": "Not logged in"}), 401

        user_id = user.get("UserId")
        keyword = request.args.get("keyword", "")

        if not keyword:
            return jsonify({"error": "Missing search keyword"}), 400

        results = SearchServiceController.search(user_id, keyword)

        if isinstance(results, dict) and "error" in results:
            return jsonify(results), 500

        return jsonify(results), 200



    