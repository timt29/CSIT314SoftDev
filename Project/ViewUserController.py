from User import User

class ViewUserController:

    def get_users(name=None, email=None):
        return User.get_all_users(name=name, email=email)