from flask import request, render_template, session, jsonify, redirect
import mysql.connector

# Utility function for database connection (reuse this or import if centralised)
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="testingcsit314"
    )

class CleanerController:
    def __init__(self, app, db_connector):
        self.app = app
        self.get_db_connection = db_connector
        self.register_routes()

    def register_routes(self):
        # Add a new service
        @self.app.route("/api/cleaner/services", methods=["POST"])
        def add_service():
            user = session.get("user")
            if not user:
                return jsonify({"error": "Not logged in"}), 401

            data = request.json
            name = data.get("name")
            price = data.get("price")
            duration = data.get("duration")

            if not all([name, price, duration]):
                return jsonify({"error": "Missing required fields"}), 400

            conn = self.get_db_connection()
            cursor = conn.cursor()
            try:
                # Insert into service table
                cursor.execute("""
                    INSERT INTO service (name, price, duration)
                    VALUES (%s, %s, %s)
                """, (name, price, duration))
                service_id = cursor.lastrowid

                # Link to cleaner
                cursor.execute("""
                    INSERT INTO cleanerservice (userid, serviceid)
                    VALUES (%s, %s)
                """, (user["UserId"], service_id))

                conn.commit()
                return jsonify({"message": "Service added", "serviceid": service_id}), 201

            except mysql.connector.Error as err:
                return jsonify({"error": f"Database error: {err}"}), 500
            finally:
                cursor.close()
                conn.close()

        # Update a service
        @self.app.route("/api/cleaner/services/<int:service_id>", methods=["PUT"])
        def update_service(service_id):
            user = session.get("user")
            if not user:
                return jsonify({"error": "Not logged in"}), 401

            data = request.json
            name = data.get("name")
            price = data.get("price")
            duration = data.get("duration")

            if not all([name, price, duration]):
                return jsonify({"error": "Missing fields"}), 400

            conn = self.get_db_connection()
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    UPDATE service
                    SET name = %s, price = %s, duration = %s
                    WHERE serviceid = %s
                """, (name, price, duration, service_id))
                conn.commit()

                if cursor.rowcount == 0:
                    return jsonify({"error": "Service not found"}), 404

                return jsonify({"message": "Service updated successfully"}), 200
            except mysql.connector.Error as err:
                return jsonify({"error": f"Database error: {err}"}), 500
            finally:
                cursor.close()
                conn.close()

        # Delete a service
        @self.app.route("/api/cleaner/services/<int:service_id>", methods=["DELETE"])
        def delete_service(service_id):
            user = session.get("user")
            if not user:
                return jsonify({"error": "Not logged in"}), 401

            conn = self.get_db_connection()
            cursor = conn.cursor()
            try:
                cursor.execute("DELETE FROM cleanerservice WHERE serviceid = %s", (service_id,))
                cursor.execute("DELETE FROM service WHERE serviceid = %s", (service_id,))
                conn.commit()

                if cursor.rowcount == 0:
                    return jsonify({"error": "Service not found"}), 404

                return jsonify({"message": "Service deleted successfully"}), 200
            except mysql.connector.Error as err:
                return jsonify({"error": f"Database error: {err}"}), 500
            finally:
                cursor.close()
                conn.close()
