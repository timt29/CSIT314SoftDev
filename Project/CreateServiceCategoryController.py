from ServiceCategory import ServiceCategory

class CreateServiceCategoryController:
    @staticmethod
    def create_service_category(CategoryName):
        return ServiceCategory.create_servicecategory(CategoryName)