import mysql.connector
from flask import session
def get_service_history(service_id=None, date_used=None):
    try:
        user = session.get("user")
        if not user:
            return []

        homeowner_id = user.get("UserId")

        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",
            database="testingcsit314",
            port=3306,
            auth_plugin='mysql_native_password'
        )
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT 
            h.date_used, 
            c.name AS cleaner_name, 
            s.name AS service_name, 
            s.price
        FROM history h
        JOIN cleaner c ON h.cleanerid = c.userid
        JOIN service s ON h.serviceid = s.serviceid
        WHERE h.homeownerid = %s
        """
        params = [homeowner_id]
        if service_id:
            query += " AND s.serviceid = %s"
            params.append(service_id)

        if date_used:
            query += " AND DATE(h.date_used) = %s"
            params.append(date_used)

        query += " ORDER BY h.date_used DESC"
        cursor.execute(query, params)
        return cursor.fetchall()

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
        return []
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
