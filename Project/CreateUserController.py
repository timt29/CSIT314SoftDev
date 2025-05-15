from User import User

class CreateUserController:
    @staticmethod
    def create_user(email, name, password, role, dob, status="Active"):
        return User.create_user(email, name, password, role, dob, status)