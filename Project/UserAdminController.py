from flask import request, render_template, redirect, url_for, session, jsonify
import mysql.connector

# Local DB connector now embedded here
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",         
        password="password",    
        database="csit314"
    )

def login_controller(app):
    @app.route("/", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            email = request.form["email"]
            password = request.form["password"]
            role = request.form["role"]

            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM users WHERE email = %s AND password = %s AND role = %s",
                (email, password, role)
            )
            user = cursor.fetchone()
            cursor.close()
            conn.close()

            if user:
                session["user"] = user
                if role == "Admin User":
                    return redirect(url_for("admin_dashboard"))
                elif role == "Cleaner":
                    return redirect(url_for("cleaner_dashboard"))
                elif role == "Home Owner":
                    return redirect(url_for("home"))
                elif role == "Platform Management":
                    return redirect(url_for("platform_dashboard"))
            else:
                return render_template("login.html", error="Invalid credentials or role")

        return render_template("login.html")


def dashboard_routes(app):
    @app.route("/dashboard_admin")
    def admin_dashboard():
        return render_template("dashboard_admin.html")

    @app.route("/dashboard_cleaner")
    def cleaner_dashboard():
        return render_template("dashboard_cleaner.html")

    @app.route("/dashboard_platform")
    def platform_dashboard():
        return render_template("dashboard_platform.html")


def user_data_api(app):
    @app.route("/users", methods=["GET"])
    def get_users():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(users)

    @app.route("/register", methods=["POST"])
    def register_user():
        data = request.json
        valid_roles = ["Cleaner", "Admin User", "Platform Management", "Home Owner"]

        # Validate the role
        if data["role"] not in valid_roles:
            return jsonify({"message": "Invalid role"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (email, password, username, role, dob)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            data["email"],
            data["password"],
            data["username"],
            data["role"],
            data["dob"]
        ))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "User registered successfully"}), 201

    @app.route("/api/users/<int:user_id>", methods=["PUT"])
    def update_user(user_id):
        data = request.json

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE users
            SET username = %s, email = %s
            WHERE user_id = %s
        """, (
            data["username"],
            data["email"],
            user_id
        ))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "User updated successfully"}), 200
