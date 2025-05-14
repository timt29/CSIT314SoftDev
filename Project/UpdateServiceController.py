from Service import Service

class UpdateServiceController:

    def update_service(service_id, name, price, duration):
        success, message = Service.update_service(service_id, name, price, duration)
        if not success:
            return {"error": message}, 404 if message == "Service not found" else 500
        return {"message": message}, 200