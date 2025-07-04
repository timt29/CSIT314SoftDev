import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="testingcsit314"
    )

class Favourite:
    def __init__(self, db_connector):
        get_db_connection = db_connector

    def get_favourite_cleaners(homeowner_id: int):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT
            c.name AS cleaner_name,
            s.name AS service_name,
            s.price AS price
        FROM favourite f
        JOIN cleaner c ON f.cleanerid = c.userid
        JOIN service s ON f.serviceid = s.serviceid
        WHERE f.homeownerid = %s
        """
        cursor.execute(query, (homeowner_id,))
        return cursor.fetchall()

    def get_homeowner_name(user_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT name FROM homeowner WHERE userid = %s", (user_id,))
        result = cursor.fetchone()
        return result["name"] if result else None