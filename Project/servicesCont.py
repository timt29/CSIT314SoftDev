import mysql.connector

def get_services():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",
            database="csit314",
            port=3306,
            auth_plugin='mysql_native_password'
        )
        cursor = conn.cursor(dictionary=True)  # Return results as dictionaries for easier access
        cursor.execute("SELECT  name, pricing, duration FROM service")
        cleaners = cursor.fetchall()
        return cleaners
    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
        return []  # Return empty list on error
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()