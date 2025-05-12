# favController.py

import mysql.connector
from flask import session

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
