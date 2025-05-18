from ServiceCategory import ServiceCategory

class CreateServiceCategoryController:
    @staticmethod
    def createServiceCategory(CategoryName):
        return ServiceCategory.createServiceCategory(CategoryName)