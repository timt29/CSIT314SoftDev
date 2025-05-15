from User import User

class SearchController:
    @staticmethod
    def search_users(search_query):
        return User.search_users(search_query)
