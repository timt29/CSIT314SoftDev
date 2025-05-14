import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="testingcsit314"
    )

class History:
    def __init__(self, db_connector):
        get_db_connection = db_connector

    def get_homeowner_name(user_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT name FROM homeowner WHERE userid = %s", (user_id,))
        result = cursor.fetchone()
        return result["name"] if result else None


    def get_service_history(homeowner_id, service_id=None, date_used=None):
        conn = get_db_connection()
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
