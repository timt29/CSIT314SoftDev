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
            search_query = request.args.get("search", "").strip()  # Get the search query from the request
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            if search_query:
                # Search by name or email
                cursor.execute("""
                    SELECT * FROM users
                    WHERE name LIKE %s OR email LIKE %s
                """, (f"%{search_query}%", f"%{search_query}%"))
            else:
                # Fetch all users if no search query is provided
                cursor.execute("SELECT * FROM users")

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
            new_email = data.get("new_email", email)  # Default to the current email if not provided
            name = data.get("name")  # Name can be None if not provided
            role = data.get("role")  # Role can be None if not provided

            try:
                conn = get_db_connection()
                cursor = conn.cursor()

                # Check if the new email already exists (only if the email is being changed)
                if new_email != email:
                    cursor.execute("SELECT * FROM users WHERE email = %s", (new_email,))
                    existing_user = cursor.fetchone()
                    if existing_user:
                        return jsonify({"error": "Email already in use"}), 409

                # Build the SQL query dynamically based on the fields provided
                update_fields = []
                update_values = []

                if new_email != email:
                    update_fields.append("email = %s")
                    update_values.append(new_email)
                if name:
                    update_fields.append("name = %s")
                    update_values.append(name)
                if role:
                    update_fields.append("role = %s")
                    update_values.append(role)

                # Add the current email to the WHERE clause
                update_values.append(email)

                # Execute the update query
                if update_fields:
                    query = f"UPDATE users SET {', '.join(update_fields)} WHERE email = %s"
                    cursor.execute(query, tuple(update_values))
                    conn.commit()

                if cursor.rowcount == 0:
                    return jsonify({"error": "User not found"}), 404

                cursor.close()
                conn.close()

                return jsonify({"message": "User updated successfully"}), 200

            except mysql.connector.Error as err:
                return jsonify({"error": f"Database error: {err}"}), 500
            except Exception as e:
                return jsonify({"error": f"Error: {str(e)}"}), 500

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
            conn = get_db_connection()
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

    @app.route("/logout", methods=["GET"])
    def logout():
        session.clear()  # Clear the session
        return redirect(url_for("login"))  # Redirect to the login page


# Cleaner Dashboard Route
def dashboard_routes(app):
    @app.route("/dashboard_cleaner")
    def cleaner_dashboard():
        return render_template("dashboard_cleaner.html")

    @app.route("/dashboard_platform")
    def platform_dashboard():
        return render_template("dashboard_platform.html")
