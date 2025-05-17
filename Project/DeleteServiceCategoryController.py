from ServiceCategory import ServiceCategory

class DeleteServiceCategoryController:
    @staticmethod
    def delete_by_category(CategoryName):
        return ServiceCategory.delete_by_category(CategoryName)