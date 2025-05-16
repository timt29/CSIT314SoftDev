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
        self.register_routes()
    
    @staticmethod
    def get_cleaner_popularity_report():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT c.name AS cleaner_name, s.name AS service_name, COUNT(h.historyid) AS times_booked
            FROM cleaner c
            JOIN cleanerservice cs ON c.userid = cs.userid
            JOIN service s ON cs.serviceid = s.serviceid
            LEFT JOIN history h ON h.cleanerid = c.userid AND h.serviceid = s.serviceid
            GROUP BY c.userid, s.serviceid
            ORDER BY times_booked DESC
        """)
        report = cursor.fetchall()
        cursor.close()
        conn.close()
        return report

    @staticmethod
    def get_cleaner_service_usage_report():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT c.name AS cleaner_name, COUNT(cs.serviceid) AS num_services
            FROM cleaner c
            LEFT JOIN cleanerservice cs ON c.userid = cs.userid
            GROUP BY c.userid
            ORDER BY num_services DESC
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
            SELECT h.name AS homeowner_name,
                COUNT(DISTINCT f.cleanerid) AS num_favourites,
                COUNT(DISTINCT hi.historyid) AS num_bookings
            FROM homeowner h
            LEFT JOIN favourite f ON h.userid = f.homeownerid
            LEFT JOIN history hi ON h.userid = hi.homeownerid
            GROUP BY h.userid
            ORDER BY num_bookings DESC, num_favourites DESC
        """)
        report = cursor.fetchall()
        cursor.close()
        conn.close()
        return report