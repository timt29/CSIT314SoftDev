# favController.py

import mysql.connector
from flask import session

def get_favourite_cleaners():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",  # Replace with your actual password
            database="csit314",
            port=3306,
            auth_plugin='mysql_native_password'
        )
        cursor = conn.cursor(dictionary=True)

        homeowner_id = session.get("homeowner_id")
        if not homeowner_id:
            return []  # No logged-in user

        query = """
            SELECT c.userid, c.name, c.experience, c.service
            FROM favourite f
            JOIN cleaner c ON f.cleaner_id = c.userid
            WHERE f.homeowner_id = %s
            ORDER BY f.date_saved DESC
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
