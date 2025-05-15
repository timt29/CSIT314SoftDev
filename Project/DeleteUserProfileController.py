from UserProfile import UserProfile

class DeleteUserProfileController:
    @staticmethod
    def delete_profile(role):
        return UserProfile.delete_by_role(role)