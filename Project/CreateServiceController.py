from Service import Service

class CreateServiceController:

    def add_service(user_id, name, price, duration):
        return Service.add_service(user_id, name, price, duration)