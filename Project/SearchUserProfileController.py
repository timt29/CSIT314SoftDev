from UserProfile import UserProfile

class SearchUserProfileController:
    @staticmethod
    def search_profiles(query):
        return UserProfile.search(query)
