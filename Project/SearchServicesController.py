from flask import request

class SearchServicesController:

    def get_search_input():
        return {
            "search_query": request.form.get("search_query", "").strip(),
            "service_filter": request.form.get("service_filter", "")
        }
