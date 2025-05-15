from flask import session, redirect, url_for

class LogoutController:

    @staticmethod
    def logout():
        session.clear()
        return redirect(url_for("login"))
