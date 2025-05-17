from ServiceCategory import ServiceCategory

class SearchServiceCategoryController:
    @staticmethod
    def searchcategory(query):
        return ServiceCategory.searchcategory(query)