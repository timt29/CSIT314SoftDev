from Number import Number

class ViewCountController:

    def increaseViewCount(cleaner_id, service_id):
        return Number.increment_view_count(cleaner_id, service_id)