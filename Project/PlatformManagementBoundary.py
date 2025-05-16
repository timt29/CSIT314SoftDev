from flask import request, render_template, redirect, session, jsonify
from PlatformManagementController import PlatformManagementController

def register_routes7(app):

    @app.route("/platform/home")
    def platform_home():
        user = session.get("user")
        if not user or user.get("role") != "Platform Management":
            return redirect('/')
        
        stats = PlatformManagementController.get_platform_stats()
        return render_template("dashboard_platform.html", stats=stats)

    @app.route('/api/report/cleaner_popularity')
    def api_cleaner_popularity():
        data = Report.get_cleaner_popularity_report()
        return jsonify(data)

    @app.route('/api/report/homeowner_engagement')
    def api_homeowner_engagement():
        data = Report.get_homeowner_engagement_report()
        return jsonify(data)