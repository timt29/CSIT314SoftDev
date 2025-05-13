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

class FavouriteController:
    def __init__(self, app, db_connector):
        self.app = app
        self.get_db_connection = db_connector
        self.register_routes()

    def register_routes(self):
        @self.app.route('/fav')
        def favourites_page():
            user = session.get("user")
            if not user:
                return redirect('/')

            user_id = user.get("UserId")
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute("SELECT name FROM homeowner WHERE userid = %s", (user_id,))
            homeowner = cursor.fetchone()

            if not homeowner:
                return "homeowner not found", 404
            cleaners = get_favourite_cleaners(user_id)
            return render_template(
                'HOfav.html',
                favourites=cleaners,
                homeowner_name=homeowner["name"])


def get_favourite_cleaners(homeowner_id :int):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",  # Replace with your actual password
            database="testingcsit314",
            port=3306,
            auth_plugin='mysql_native_password'
        )
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT
                c.name AS cleaner_name,
                s.price,
                s.name AS service_name
            FROM
                testingcsit314.favourite f
            JOIN
                testingcsit314.cleaner c ON f.cleanerid = c.userid
            JOIN
                testingcsit314.cleanerservice cs ON c.userid = cs.userid
            JOIN
                testingcsit314.service s ON cs.serviceid = s.serviceid
            WHERE
                f.homeownerid = %s
        """
        cursor.execute(query, (homeowner_id,))
        favourites = cursor.fetchall()
        return favourites

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
        return []

    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
