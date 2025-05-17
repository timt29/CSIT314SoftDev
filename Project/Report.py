import mysql.connector
from flask import render_template


def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="testingcsit314"
    )

class Report:
    def __init__(self, app, db_connector):
        self.app = app
        self.get_db_connection = db_connector
       # self.register_routes()
    
    def getPM_id(user_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT name FROM users WHERE userid = %s", (user_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result

    def get_cleaner_popularity_report():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
           SELECT c.UserId AS CleanerId, u.Name AS CleanerName,
           s.ServiceId, s.Name AS ServiceName, COUNT(b.BookingId) AS BookingCount
           FROM cleanerservice cs 
           JOIN cleaner c ON cs.UserId = c.UserId
           JOIN users u ON c.UserId = u.UserId
           JOIN service s ON cs.ServiceId = s.ServiceId
           LEFT JOIN booking b ON cs.UserId = b.CleanerId AND cs.ServiceId = b.ServiceId
           GROUP BY c.UserId, u.Name, s.ServiceId, s.Name
           ORDER BY c.UserId, s.ServiceId;

        """)
        report = cursor.fetchall()
        cursor.close()
        conn.close()
        return report

    def get_cleaner_service_usage_report():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
           SELECT 
    c.UserId AS CleanerId,
    u.Name AS CleanerName,
    COUNT(DISTINCT cs.ServiceId) AS ServicesOffered
    FROM cleanerservice cs
    JOIN cleaner c ON cs.UserId = c.UserId
    JOIN users u ON c.UserId = u.UserId
    GROUP BY c.UserId, u.Name
    ORDER BY c.UserId;
        """)
        report = cursor.fetchall()
        cursor.close()
        conn.close()
        return report

    @staticmethod
    def get_homeowner_engagement_report():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
          SELECT h.UserId AS HomeOwnerId, u.Name AS HomeOwnerName,
          f.CleanerId, cu.Name AS CleanerName, s.ServiceId,
          s.Name AS ServiceName,
          COUNT(b.BookingId) AS BookingCount
          FROM favourite f
          JOIN 
          homeowner h ON f.HomeOwnerId = h.UserId
          JOIN 
          users u ON h.UserId = u.UserId
          JOIN 
          cleaner c ON f.CleanerId = c.UserId
          JOIN 
          users cu ON c.UserId = cu.UserId
          JOIN 
          service s ON f.ServiceId = s.ServiceId
          LEFT JOIN 
          booking b ON f.HomeOwnerId = b.HomeOwnerId 
          AND f.CleanerId = b.CleanerId 
          AND f.ServiceId = b.ServiceId
          GROUP BY h.UserId, u.Name, f.CleanerId, cu.Name, s.ServiceId, s.Name
          ORDER BY h.UserId, f.CleanerId, s.ServiceId;
        """)
        report = cursor.fetchall()
        cursor.close()
        conn.close()
        return report