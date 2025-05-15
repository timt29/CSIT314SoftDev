from UserProfile import UserProfile

class ViewUserProfileController:

    @staticmethod
    def get_profiles(search_query=None):
        return UserProfile.get_user_profiles(search_query)
