from Number import Number

class ViewShortlistController:
    def add_to_favourites(homeowner_id, cleaner_id, service_id):
        return Number.add_favourite(homeowner_id, cleaner_id, service_id)
    
    def increaseShortlistCount(cleaner_id, service_id):
        return Number.increment_shortlist_count(cleaner_id, service_id)

    
