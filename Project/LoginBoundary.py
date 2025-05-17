from flask import render_template, request, session, redirect, url_for
from LoginController import LoginController

def register_login_routes(app):
    @app.route("/", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            email = request.form.get("email")
            password = request.form.get("password")
            role = request.form.get("role")

            # Use the controller to authenticate the user
            user = LoginController.authenticate_user(email, password, role)

            if user:
                if user.get("Status") == "Suspended":
                    return render_template("login.html", error="Your account is suspended. Please contact support.")
                session["user"] = user
                if role == "Admin User":
                    return redirect(url_for("admin_dashboard"))
                elif role == "Cleaner":
                    return redirect(url_for("cleaner_dashboard"))
                elif role == "Home Owner":
                    return redirect(url_for("home"))
                elif role == "Platform Management":
                    return redirect(url_for("platform_home"))
            else:
                return render_template("login.html", error="Wrong Profile, Email or Password or Suspended")

        return render_template("login.html")