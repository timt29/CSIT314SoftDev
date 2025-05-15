from User import User

class SuspendUserController:

    @staticmethod
    def suspend_user(email):
        return User.suspend_user_by_email(email)
