from ServiceCategory import ServiceCategory

class DeleteServiceCategoryController:
    @staticmethod
    def deleteServiceCategory(CategoryName):
        return ServiceCategory.deleteServiceCategory(CategoryName)