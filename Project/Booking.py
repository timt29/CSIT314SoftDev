import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="testingcsit314"
    )

class Booking:
    def __init__(self, db_connector):
        get_db_connection = db_connector

    def get_confirmed_bookings_for_cleaner(cleaner_id, service_id=None, date_used = None):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT b.BookingId,
            b.Date_Used,
            s.Name AS service_name,
            s.Price AS price,
            c.Name AS cleaner_name,
            h.Name AS homeowner_name,
            b.ServiceId,
            b.HomeOwnerId,
            b.CleanerId
            FROM booking b
            JOIN service s ON b.ServiceId = s.ServiceId
            JOIN cleaner c ON b.CleanerId = c.UserId
            JOIN homeowner h ON b.HomeOwnerId = h.UserId
            WHERE b.CleanerId = %s
                """
        params = [cleaner_id]

        if service_id:
            query += " AND b.ServiceId = %s"
            params.append(service_id)

        if date_used:
            query += " AND b.Date_Used = %s"
            params.append(date_used)

        query += " ORDER BY b.Date_Used DESC"

        cursor.execute(query, params)
        bookings = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return bookings
    

    def get_services_by_cleaner(cleaner_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT DISTINCT s.ServiceId, s.Name
            FROM booking b
            JOIN service s ON b.ServiceId = s.ServiceId
            WHERE b.CleanerId = %s
        """
        
        cursor.execute(query, (cleaner_id,))
        services = cursor.fetchall()
        cursor.close()
        conn.close()

        return services
    
    def create_booking(home_owner_id, cleaner_id, service_id):
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute("""
                INSERT INTO booking (HomeOwnerId, CleanerId, ServiceId, Date_Used) 
                VALUES (%s, %s, %s,CURDATE())
            """, (home_owner_id, cleaner_id, service_id))
            conn.commit()

            # Check if the booking was successful
            if cursor.rowcount > 0:
                return True
            else:
                return False

        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            return False
        finally:
            cursor.close()
            conn.close()