from Report import Report

class PlatformManagementController:
    @staticmethod
    def get_cleaner_popularity_report():
        # Calls the entity to get the report data
        return Report.get_cleaner_popularity_report()

    @staticmethod
    def get_cleaner_service_usage_report():
        return Report.get_cleaner_service_usage_report()

    @staticmethod
    def get_homeowner_engagement_report():
        return Report.get_homeowner_engagement_report()