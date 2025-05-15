from User import User

class UpdateUserController:
    @staticmethod
    def update_user(current_email, new_email=None, name=None, role=None):
        return User.update_user_by_email(current_email, new_email, name, role)
