from Service import Service

class ViewServiceController:

    def get_service(user_id):
        return Service.get_services_for_cleaner(user_id)