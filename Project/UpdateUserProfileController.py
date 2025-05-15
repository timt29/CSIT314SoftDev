from UserProfile import UserProfile

class UpdateUserProfileController:
    @staticmethod
    def update_description(role, description):
        return UserProfile.update_profile_description(role, description)
