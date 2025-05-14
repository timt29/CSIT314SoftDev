import mysql.connector

@staticmethod
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="testingcsit314"
    )


class HomeOwner:
    def __init__(self, db_connector):
        get_db_connection = db_connector

    def fetch_services():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT serviceid, name FROM service ORDER BY name")
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results

    def fetch_homeowner_by_id(user_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT name FROM homeowner WHERE userid = %s", (user_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result
        
    def fetch_cleaners_by_name_service(name_query=None, service_id=None):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT DISTINCT c.userid, c.name AS cleaner_name, s.name AS service_name,
                            s.price, s.duration
            FROM cleaner c
            JOIN cleanerservice cs ON c.UserId = cs.UserId
            JOIN service s ON cs.ServiceId = s.ServiceId
            WHERE 1=1
        """
        params = []
        if name_query:
            query += " AND c.name LIKE %s"
            params.append(f"%{name_query}%")
        if service_id:
            query += " AND s.ServiceId = %s"
            params.append(service_id)
        query += " ORDER BY c.name ASC"
        cursor.execute(query, tuple(params))
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results

    def fetch_all_cleaners():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT c.userid, c.name as cleaner_name, s.serviceid, s.name as service_name,
                s.price, s.duration, CONCAT('$', s.price) as formatted_price
            FROM cleaner c
            LEFT JOIN cleanerservice cs ON c.UserId = cs.UserId
            LEFT JOIN service s ON cs.serviceid = s.serviceid
            ORDER BY c.name ASC
        """
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results

    def get_cleaner_info(cleaner_id, service_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            UPDATE cleanerservice 
            SET view_count = view_count + 1 
            WHERE userid = %s AND serviceid = %s
        """, (cleaner_id, service_id))
        conn.commit()

        cursor.execute("SELECT name FROM cleaner WHERE userid = %s", (cleaner_id,))
        cleaner = cursor.fetchone()

        cursor.execute("""
            SELECT s.serviceid, s.name, s.price, s.duration, cs.view_count
            FROM service s
            JOIN cleanerservice cs ON s.serviceid = cs.serviceid
            WHERE cs.userid = %s
        """, (cleaner_id,))
        services = cursor.fetchall()

        cursor.close()
        conn.close()

        return (cleaner["name"] if cleaner else None, services)