import mysql.connector
from flask import session

def get_service_history(service_id=None, date_used=None):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",
            database="testingcsit314",
            port=3306,
            auth_plugin='mysql_native_password'
        )
        cursor = conn.cursor(dictionary=True)

        homeowner_id = session.get("homeowner_id")
        if not homeowner_id:
            return []

        query = """
        SELECT h.date_used, c.name AS cleaner_name, s.name AS service_name, s.pricing
        FROM history h
        JOIN cleaner c ON h.cleaner_id = c.userid
        JOIN cleaner_services cs ON c.userid = cs.cleaner_id
        JOIN service s ON cs.service_id = s.service_id
        WHERE h.homeowner_id = %s
        """
        params = [homeowner_id]

        if service_id:
            query += " AND s.service_id = %s"
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
