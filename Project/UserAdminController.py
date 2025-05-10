from flask import request, render_template, redirect, url_for, session, jsonify
import mysql.connector

# Utility function for database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="testingcsit314"
    )

class AdminController:
    def __init__(self, app, db_connector):
        self.app = app
        self.get_db_connection = db_connector
        self.register_routes()

    def register_routes(self):
        # Admin Dashboard Route
        @self.app.route("/dashboard_admin")
        def admin_dashboard():
            return render_template("dashboard_admin.html")

        # Get All Users
        @self.app.route("/api/users", methods=["GET"])
        def get_users():
            conn = self.get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Users")
            users = cursor.fetchall()
            cursor.close()
            conn.close()
            return jsonify(users)

        # Register a New User
        @self.app.route("/register", methods=["POST"])
        def register_user():
            data = request.json
            try:
                conn = get_db_connection()
                cursor = conn.cursor()

                # Insert into Users table
                cursor.execute("""
                    INSERT INTO Users (Email, Name, Password, Role, DoB, Status)
                    VALUES (%s, %s, %s, %s, %s, 'active')
                """, (
                    data["email"],
                    data["name"],
                    data["password"],
                    data["role"],
                    data["dob"]
                ))
                conn.commit()

                # Get the UserId of the newly created user
                user_id = cursor.lastrowid

                # Insert into the appropriate role-specific table
                if data["role"] == "Platform Management":
                    cursor.execute("""
                        INSERT INTO PlatformManagement (UserId, Name, Role)
                        VALUES (%s, %s, %s)
                    """, (user_id, data["name"], data["role"]))
                elif data["role"] == "Home Owner":
                    cursor.execute("""
                        INSERT INTO HomeOwner (UserId, Name, Role)
                        VALUES (%s, %s, %s)
                    """, (user_id, data["name"], data["role"]))
                elif data["role"] == "Cleaner":
                    cursor.execute("""
                        INSERT INTO Cleaner (UserId, Name, Role)
                        VALUES (%s, %s, %s)
                    """, (user_id, data["name"], data["role"]))
                elif data["role"] == "Admin User":
                    cursor.execute("""
                        INSERT INTO UserAdmin (UserId, Name, Role)
                        VALUES (%s, %s, %s)
                    """, (user_id, data["name"], data["role"]))

                conn.commit()
                return jsonify({"message": "User registered successfully"}), 201
            except mysql.connector.Error as err:
                return jsonify({"message": f"Database error: {err}"}), 500
            finally:
                cursor.close()
                conn.close()

        # Update User
        @self.app.route("/api/users/<string:email>", methods=["PUT"])
        def update_user(email):
            data = request.json
            try:
                conn = self.get_db_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE Users
                    SET Name = %s, Role = %s
                    WHERE Email = %s
                """, (
                    data["name"],
                    data["role"],
                    email
                ))
                if cursor.rowcount == 0:
                    return jsonify({"message": "User not found"}), 404
                conn.commit()
                return jsonify({"message": "User updated successfully"}), 200
            except mysql.connector.Error as err:
                return jsonify({"message": f"Database error: {err}"}), 500
            finally:
                cursor.close()
                conn.close()

        # Suspend User
        @self.app.route("/api/users/<string:email>/suspend", methods=["PATCH"])
        def suspend_user(email):
            try:
                conn = self.get_db_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE Users
                    SET Status = 'suspended'
                    WHERE Email = %s
                """, (email,))
                if cursor.rowcount == 0:
                    return jsonify({"message": "User not found"}), 404
                conn.commit()
                return jsonify({"message": "User suspended successfully"}), 200
            except mysql.connector.Error as err:
                return jsonify({"message": f"Database error: {err}"}), 500
            finally:
                cursor.close()
                conn.close()

        # Manage User Profiles (GET and POST)
        @self.app.route("/api/user_profiles", methods=["GET", "POST"])
        def manage_user_profiles():
            conn = self.get_db_connection()
            cursor = conn.cursor(dictionary=True)

            if request.method == "GET":
                cursor.execute("SELECT * FROM UserProfile")
                profiles = cursor.fetchall()
                cursor.close()
                conn.close()
                return jsonify(profiles)

            elif request.method == "POST":
                data = request.json
                try:
                    cursor.execute("""
                        INSERT INTO UserProfile (Role, Description)
                        VALUES (%s, %s)
                    """, (data["role"], data["description"]))
                    conn.commit()
                    return jsonify({"message": "User profile created successfully"}), 201
                except mysql.connector.Error as err:
                    return jsonify({"message": f"Database error: {err}"}), 500
                finally:
                    cursor.close()
                    conn.close()

# Login Controller
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

    @app.route("/logout", methods=["POST"])
    def logout():
        print("Logout endpoint called")  # Debugging log
        session.clear()
        return jsonify({"message": "Logged out successfully"}), 200

# Cleaner Dashboard Route
def dashboard_routes(app):
    @app.route("/dashboard_cleaner")
    def cleaner_dashboard():
        return render_template("dashboard_cleaner.html")

    @app.route("/dashboard_platform")
    def platform_dashboard():
        return render_template("dashboard_platform.html")
