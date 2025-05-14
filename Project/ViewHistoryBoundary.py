from flask import request, render_template, redirect, url_for, session, jsonify
from ViewHistoryController import ServiceHistoryController
from ViewServicesController import ViewServicesController


def register_routes3(app):
    
    @app.route("/history")
    def view_history():
        user = session.get("user")
        if not user:
            return redirect('/')

        user_id = user.get("UserId")
        homeowner_name = ViewServicesController.get_homeowner_name(user_id)["name"]
        if not homeowner_name:
            return "homeowner not found", 404

        filters = ServiceHistoryController.parse_history_filters(request)
        history = ServiceHistoryController.fetch_history(user_id, filters)
        services = ViewServicesController.get_all_services()

        return render_template(
            "history.html",
            history=history,
            services=services,
            selected_service=filters.get("service_id"),
            date_used=filters.get("date_used", ""),
            homeowner_name=homeowner_name
        )