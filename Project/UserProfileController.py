from flask import request, jsonify
import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="testingcsit314"
    )

class UserProfileController:
    def __init__(self, app, db_connector):
        self.app = app
        self.get_db_connection = db_connector
        self.register_routes()

    def register_routes(self):
        # Get all user profiles
        @self.app.route("/api/user_profiles", methods=["GET"])
        def get_user_profiles():
            conn = self.get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM UserProfile;")
            profiles = cursor.fetchall()
            cursor.close()
            conn.close()
            return jsonify(profiles)

        # Create a new user profile
        @self.app.route("/api/user_profiles", methods=["POST"])
        def create_user_profile():
            data = request.json
            role = data.get("role")
            description = data.get("description")

            if not role or not description:
                return jsonify({"error": "Missing role or description"}), 400

            conn = self.get_db_connection()
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "INSERT INTO UserProfile (Role, Description) VALUES (%s, %s)",
                    (role, description)
                )
                conn.commit()
            except mysql.connector.IntegrityError:
                conn.rollback()
                return jsonify({"error": "Role already exists"}), 409
            finally:
                cursor.close()
                conn.close()

            return jsonify({"message": "User profile created successfully"}), 201

        # Update an existing user profile
        @self.app.route("/api/user_profiles/<string:role>", methods=["PUT"])
        def update_user_profile(role):
            data = request.json
            description = data.get("description")

            if not description:
                return jsonify({"error": "Missing description"}), 400

            conn = self.get_db_connection()
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "UPDATE UserProfile SET Description = %s WHERE Role = %s",
                    (description, role)
                )
                if cursor.rowcount == 0:
                    return jsonify({"error": "Role not found"}), 404
                conn.commit()
            finally:
                cursor.close()
                conn.close()

            return jsonify({"message": "User profile updated successfully"}), 200

        # Delete a user profile
        @self.app.route("/api/user_profiles/<string:role>", methods=["DELETE"])
        def delete_user_profile(role):
            conn = self.get_db_connection()
            cursor = conn.cursor()
            try:
                cursor.execute("DELETE FROM UserProfile WHERE Role = %s", (role,))
                if cursor.rowcount == 0:
                    return jsonify({"error": "Role not found"}), 404
                conn.commit()
            finally:
                cursor.close()
                conn.close()

            return jsonify({"message": "User profile deleted successfully"}), 200
