from ServiceCategory import ServiceCategory

class UpdateServiceCategoryController:
    @staticmethod
    def update_service_category(CategoryName):
        return ServiceCategory.update_service_category(CategoryName)