import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="testingcsit314"
    )

class User:
    def __init__(self, db_connector):
        get_db_connection = db_connector

    def get_all_users(name=None, email=None):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        name = name if name else None
        email = email if email else None

        if name and email:
            cursor.execute("""
                SELECT * FROM users
                WHERE name LIKE %s OR email LIKE %s
            """, (f"%{name}%", f"%{email}%"))
        elif name:
            cursor.execute("""
                SELECT * FROM users
                WHERE name LIKE %s
            """, (f"%{name}%",))
        elif email:
            cursor.execute("""
                SELECT * FROM users
                WHERE email LIKE %s
            """, (f"%{email}%",))
        else:
            cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        print("Fetched users:", users)
        cursor.close()
        conn.close()
        return users