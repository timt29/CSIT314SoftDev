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

    def update_service(service_id, name, price, duration):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE service
                SET name = %s, price = %s, duration = %s
                WHERE serviceid = %s
            """, (name, price, duration, service_id))
            conn.commit()

            if cursor.rowcount == 0:
                return False, "Service not found"

            return True, "Service updated successfully"

        except mysql.connector.Error as err:
            return False, f"Database error: {err}"

        finally:
            cursor.close()
            conn.close()

    def delete_service(service_id):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Delete from cleanerservice first due to FK constraint
            cursor.execute("DELETE FROM cleanerservice WHERE serviceid = %s", (service_id,))
            cursor.execute("DELETE FROM service WHERE serviceid = %s", (service_id,))
            conn.commit()

            if cursor.rowcount == 0:
                return False, "Service not found"

            return True, "Service deleted successfully"

        except mysql.connector.Error as err:
            return False, f"Database error: {err}"

        finally:
            cursor.close()
            conn.close()

    def search_services(user_id, keyword):
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            query = """
                SELECT s.serviceid, s.name, s.price, s.duration,
                       cs.view_count, cs.shortlist_count
                FROM service s
                JOIN cleanerservice cs ON s.serviceid = cs.serviceid
                WHERE cs.userid = %s AND s.name LIKE %s
            """
            cursor.execute(query, (user_id, f"%{keyword}%",))
            results = cursor.fetchall()

            return results

        except mysql.connector.Error as err:
            return {"error": f"Database error: {err}"}

        finally:
            cursor.close()
            conn.close()