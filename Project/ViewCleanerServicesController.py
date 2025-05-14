from homeowner import HomeOwner

class ViewCleanerServicesController:


    def get_all_services():
        return HomeOwner.fetch_services()

    def get_homeowner_name(user_id):
        return HomeOwner.fetch_homeowner_by_id(user_id)
    
    def get_cleaners(name_query=None, service_id=None):
        return HomeOwner.fetch_cleaners_by_name_service(name_query, service_id)

    def get_all_cleaners_with_services():
        return HomeOwner.fetch_all_cleaners()
