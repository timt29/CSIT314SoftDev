from Service import Service

class SearchServiceController:

    def search(user_id, keyword):
        return Service.search_services(user_id, keyword)