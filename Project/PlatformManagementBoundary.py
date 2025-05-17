from flask import request, render_template, redirect, session, jsonify
from PlatformManagementController import PlatformManagementController

def register_routes7(app):

    @app.route("/platform/home")
    def platform_home():
        user = session.get("user")
        #print("DEBUG: session user =", user)  # Add this line
        if not user:
            return redirect('/')
        user_id = user.get("UserId")
        PM = PlatformManagementController.get_PM_ID(user_id)

        return render_template("dashboard_platform.html", PM=PM["name"])

    @app.route('/api/report/cleaner_popularity')
    def api_cleaner_popularity():
        data = PlatformManagementController.get_cleaner_popularity_report()
        return jsonify(data)

    @app.route('/api/report/cleaner_service_usage')
    def api_cleaner_service_usage():
        data = PlatformManagementController.get_cleaner_service_usage_report()
        return jsonify(data)
    
    @app.route('/api/report/homeowner_engagement')
    def api_homeowner_engagement():
        data = PlatformManagementController.get_homeowner_engagement_report()
        return jsonify(data)