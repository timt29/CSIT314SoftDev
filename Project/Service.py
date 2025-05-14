import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="testingcsit314"
    )

class Service:
    def __init__(self, db_connector):
        get_db_connection = db_connector

    def get_services_for_cleaner(user_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT s.serviceid, s.name, s.price, s.duration,
                   cs.view_count, cs.shortlist_count
            FROM service s
            JOIN cleanerservice cs ON s.serviceid = cs.serviceid
            WHERE cs.userid = %s
        """, (user_id,))  # proper tuple

        services = cursor.fetchall()

        cursor.close()
        conn.close()

        return services
