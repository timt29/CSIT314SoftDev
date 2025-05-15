from UserProfile import UserProfile

class CreateUserProfileController:
    @staticmethod
    def create_profile(role, description):
        return UserProfile.create_profile(role, description)