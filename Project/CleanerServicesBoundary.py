from flask import request, render_template, redirect, session
from ViewCleanerServicesController import ViewCleanerServicesController
from SearchCleanerServicesController import SearchCleanerServicesController
from ViewCountController import ViewCountController

def register_routes2(app):

    @app.route("/home")
    def home():
        user = session.get("user")
        if not user:
            return redirect('/')
        
        user_id = user.get("UserId")
        homeowner = ViewCleanerServicesController.get_homeowner_name(user_id)
        if not homeowner:
            return "homeowner not found", 404

        cleaners = ViewCleanerServicesController.get_cleaners()
        services = ViewCleanerServicesController.get_all_services()

        return render_template("HomeOwnerPg.html", cleaners=cleaners, services=services,
                            search_query="", selected_service="", homeowner_name=homeowner["name"])

    @app.route("/search", methods=["POST"])
    def search():
        user = session.get("user")
        if not user:
            return redirect('/')

        user_id = user.get("UserId")
        homeowner = ViewCleanerServicesController.get_homeowner_name(user_id)
        if not homeowner:
            return "homeowner not found", 404

        data = SearchCleanerServicesController.get_search_input()
        cleaners = ViewCleanerServicesController.get_cleaners(data["search_query"], int(data["service_filter"]) if data["service_filter"] else None)
        services = ViewCleanerServicesController.get_all_services()

        return render_template("HomeOwnerPg.html", cleaners=cleaners, services=services,
                            search_query=data["search_query"], selected_service=data["service_filter"],
                            homeowner_name=homeowner["name"])

    @app.route("/cleanerinfo")
    def cleaner_info():
        from homeowner import HomeOwner
        cleaner_id = request.args.get("cleaner_id", type=int)
        service_id = request.args.get("service_id", type=int)
        
        if not cleaner_id or not service_id:
            return "Cleaner ID and Service ID required", 400
        
        ViewCountController.increaseViewCount(cleaner_id, service_id)

        cleaner_name, services = HomeOwner.get_cleaner_info(cleaner_id)
        if not cleaner_name:
            return "Cleaner not found", 404

        return render_template("cleanerinfo.html", cleaner_name=cleaner_name, services=services, cleaner_id=cleaner_id)

    


