import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="testingcsit314"
    )

class Number:
    def __init__(self, db_connector):
        get_db_connection = db_connector

    def increment_view_count(cleaner_id, service_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            UPDATE cleanerservice 
            SET view_count = view_count + 1 
            WHERE userid = %s AND serviceid = %s
        """, (cleaner_id, service_id))
        conn.commit()
        cursor.close()

    def increment_shortlist_count(cleaner_id, service_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            UPDATE cleanerservice 
            SET shortlist_count = shortlist_count + 1 
            WHERE userid = %s AND serviceid = %s
        """, (cleaner_id, service_id))
        conn.commit()
        cursor.close()

    def add_favourite(homeowner_id, cleaner_id, service_id):
        if not (homeowner_id and cleaner_id and service_id):
            return False, "Missing required info"

        try:
            conn = get_db_connection()  # Replace with your DB connection function
            cursor = conn.cursor()

            # Check if the combination already exists in the favourites table
            cursor.execute("""
                SELECT COUNT(*) FROM favourite 
                WHERE HomeOwnerId = %s AND CleanerId = %s AND ServiceId = %s
            """, (homeowner_id, cleaner_id, service_id))

            result = cursor.fetchone()

            if result[0] > 0:
                return False, "Already shortlisted!"  # The favourite already exists

            # If not, insert the new favourite
            cursor.execute("""
                INSERT INTO favourite (HomeOwnerId, CleanerId, ServiceId)
                VALUES (%s, %s, %s)
            """, (homeowner_id, cleaner_id, service_id))

            conn.commit()
            return True, None  # Success

        except Exception as e:
            return False, str(e)

        finally:
            cursor.close()
            conn.close()