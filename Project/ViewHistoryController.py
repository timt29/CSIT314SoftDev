from History import History

class ServiceHistoryController:
    def fetch_history(homeowner_id, filters):
        service_id = filters.get("service_id")
        date_used = filters.get("date_used")
        return History.get_service_history(homeowner_id, service_id, date_used)
    
    def parse_history_filters(request):
        return {
            "service_id": request.args.get("service_filter", type=int),
            "date_used": request.args.get("date_used")
        }