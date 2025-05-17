from ServiceCategory import ServiceCategory

class ViewServiceCategoryController:
    @staticmethod
    def get_service_category(search_query=None):
        return ServiceCategory.get_service_category(search_query)