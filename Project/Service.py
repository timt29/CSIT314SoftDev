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
    
    def add_service(user_id, name, price, duration):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            # Insert into service table
            cursor.execute("""
                INSERT INTO service (name, price, duration)
                VALUES (%s, %s, %s)
            """, (name, price, duration))
            service_id = cursor.lastrowid

            # Link to cleaner
            cursor.execute("""
                INSERT INTO cleanerservice (userid, serviceid)
                VALUES (%s, %s)
            """, (user_id, service_id))

            conn.commit()
            return ({"message": "Service added", "serviceid": service_id}), 201

        except mysql.connector.Error as err:
            return ({"error": f"Database error: {err}"}), 500
        finally:
            cursor.close()
            conn.close()
