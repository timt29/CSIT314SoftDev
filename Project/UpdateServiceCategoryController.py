from ServiceCategory import ServiceCategory

class UpdateServiceCategoryController:
    @staticmethod
    def updateServiceCategory(oldCategoryName, newCategoryName):
        return ServiceCategory.updateServiceCategory(oldCategoryName, newCategoryName)