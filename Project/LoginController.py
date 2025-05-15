from User import User

class LoginController:
    @staticmethod
    def authenticate_user(email, password, role):
        return User.authenticate(email, password, role)