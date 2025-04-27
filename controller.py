from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from datetime import datetime

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Needed for session management

# 🟢 ENTITY
class User:
    def __init__(self, username, password, role, email, dob):
        self.username = username
        self.password = password
        self.role = role
        self.email = email
        self.dob = dob
        self.status = "Active"

# 🟡 CONTROLLER
class UserManager:
    users = []

    @classmethod
    def create_user(cls, username, password, role, email, dob):
        cls.users.append(User(username, password, role, email, dob))

    @classmethod
    def find_user(cls, username):
        for user in cls.users:
            if user.username == username:
                return user
        return None

    @classmethod
    def update_user(cls, username, role, email, dob):
        user = cls.find_user(username)
        if user:
            user.role = role
            user.email = email
            user.dob = dob
            return True
        return False

    @classmethod
    def suspend_user(cls, username):
        user = cls.find_user(username)
        if user:
            user.status = "Suspended"
            return True
        return False

    @classmethod
    def search_users(cls, query):
        return [user for user in cls.users if query.lower() in user.username.lower()]

    @classmethod
    def get_all_users(cls):
        return cls.users

# Create a default admin user
UserManager.create_user("admin", "admin", "Admin", "admin@example.com", "1990-01-01")


# 🟣 FLASK ROUTES (Boundary)

@app.route("/")
def login_page():
    return render_template("login.html")

@app.route("/dashboard")
def dashboard_page():
    if "username" not in session:
        return redirect(url_for("login_page"))
    return render_template("dashboard.html")

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data["username"]
    password = data["password"]
    user_type = data["userType"]

    user = UserManager.find_user(username)
    if user and user.password == password and user.role == user_type:
        session["username"] = username
        session["role"] = user.role

        if user.role == "Admin":
            redirect_page = "/dashboard/admin"
        elif user.role == "Cleaner":
            redirect_page = "/dashboard/cleaner"
        elif user.role == "Homeowner":
            redirect_page = "/dashboard/homeowner"
        elif user.role == "Platform Management":
            redirect_page = "/dashboard/platform"
        else:
            return "Invalid Role", 400

        return jsonify({"redirect": redirect_page})

    return "Invalid credentials", 401

# Dashboards
@app.route("/dashboard/admin")
def dashboard_admin():
    if session.get("role") != "Admin":
        return redirect(url_for("login_page"))
    return render_template("dashboard_admin.html")

@app.route("/dashboard/cleaner")
def dashboard_cleaner():
    if session.get("role") != "Cleaner":
        return redirect(url_for("login_page"))
    return render_template("dashboard_cleaner.html")

@app.route("/dashboard/homeowner")
def dashboard_homeowner():
    if session.get("role") != "Homeowner":
        return redirect(url_for("login_page"))
    return render_template("dashboard_homeowner.html")

@app.route("/dashboard/platform")
def dashboard_platform():
    if session.get("role") != "Platform Management":
        return redirect(url_for("login_page"))
    return render_template("dashboard_platform.html")


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login_page"))

# API for users management
@app.route("/api/users", methods=["GET", "POST"])
def users_api():
    if request.method == "POST":
        data = request.json
        UserManager.create_user(data["username"], data["password"], data["role"], data["email"], data["dob"])
        return jsonify({"message": "User created successfully"})
    else:
        users = UserManager.get_all_users()
        users_data = [{"username": u.username, "role": u.role, "email": u.email, "dob": u.dob, "status": u.status} for u in users]
        return jsonify(users_data)

@app.route("/api/users/<username>", methods=["PUT"])
def update_user_api(username):
    data = request.json
    success = UserManager.update_user(username, data["role"], data["email"], data["dob"])
    if success:
        return jsonify({"message": "User updated successfully"})
    else:
        return jsonify({"message": "User not found"}), 404

@app.route("/api/users/<username>/suspend", methods=["PATCH"])
def suspend_user_api(username):
    success = UserManager.suspend_user(username)
    if success:
        return jsonify({"message": "User suspended successfully"})
    else:
        return jsonify({"message": "User not found"}), 404

@app.route("/api/users/search")
def search_user_api():
    query = request.args.get("query", "")
    results = UserManager.search_users(query)
    users_data = [{"username": u.username, "role": u.role, "email": u.email, "dob": u.dob, "status": u.status} for u in results]
    return jsonify(users_data)

if __name__ == "__main__":
    app.run(debug=True)
