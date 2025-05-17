from Report import Report

class PlatformManagementController:
    
    def get_cleaner_popularity_report():
        return Report.get_cleaner_popularity_report()

    
    def get_cleaner_service_usage_report():
        return Report.get_cleaner_service_usage_report()

    
    def get_homeowner_engagement_report():
        return Report.get_homeowner_engagement_report()
    
    def get_PM_ID(user_id):
        return Report.getPM_id(user_id)