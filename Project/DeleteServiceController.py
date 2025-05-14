from Service import Service

class DeleteServiceController:

    def delete_service(service_id):
        success, message = Service.delete_service(service_id)
        if not success:
            return {"error": message}, 404 if message == "Service not found" else 500
        return {"message": message}, 200