import mysql.connector

class User:
    def __init__(self, db_connector):
        get_db_connection = db_connector
        
    @staticmethod
    def get_db_connection():
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",
            database="testingcsit314"
        )
    @staticmethod
    def authenticate(email, password, role):
        conn = User.get_db_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM users WHERE email = %s AND password = %s AND role = %s AND status = 'Active'",
                (email, password, role)
            )
            user = cursor.fetchone()
            return user
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_all_users(name=None, email=None):
        conn = User.get_db_connection()
        try:
            cursor = conn.cursor(dictionary=True)
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
            return users
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def create_user(email, name, password, role, dob, status="Active"):
        conn = User.get_db_connection()
        try:
            cursor = conn.cursor()
            # Insert into users table
            cursor.execute(""" 
                INSERT INTO users (email, name, password, role, dob, status)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (email, name, password, role, dob, status))
            conn.commit()
            user_id = cursor.lastrowid  # Get the auto-incremented UserId

            # Insert into the appropriate role table
            if role == "Admin User":
                cursor.execute("INSERT INTO useradmin (UserId, Name, Role) VALUES (%s, %s, %s)", (user_id, name, role))
            elif role == "Cleaner":
                cursor.execute("INSERT INTO cleaner (UserId, Name, Role) VALUES (%s, %s, %s)", (user_id, name, role))
            elif role == "Home Owner":
                cursor.execute("INSERT INTO homeowner (UserId, Name, Role) VALUES (%s, %s, %s)", (user_id, name, role))
            elif role == "Platform Management":
                cursor.execute("INSERT INTO platformmanagement (UserId, Name, Role) VALUES (%s, %s, %s)", (user_id, name, role))
            conn.commit()

            return True, "User created successfully."
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False, str(err)
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def search_users(query):
        conn = User.get_db_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT 
                    email AS Email,
                    name AS Name,
                    role AS Role,
                    dob AS DoB,
                    status AS Status
                FROM users
                WHERE LOWER(name) LIKE LOWER(%s) OR LOWER(email) LIKE LOWER(%s)
            """, (f"%{query}%", f"%{query}%"))
            users = cursor.fetchall()
            return users
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def update_user_by_email(current_email, new_email=None, name=None, role=None):
        conn = User.get_db_connection()
        try:
            cursor = conn.cursor()

            updates = []
            params = []

            if new_email and new_email != current_email:
                cursor.execute("SELECT * FROM users WHERE email = %s", (new_email,))
                if cursor.fetchone():
                    return {"error": "New email already in use"}, 409
                updates.append("email = %s")
                params.append(new_email)
            if name:
                updates.append("name = %s")
                params.append(name)
            if role:
                updates.append("role = %s")
                params.append(role)

            if not updates:
                return {"error": "No fields to update"}, 400

            update_clause = ", ".join(updates)
            params.append(current_email)

            query = f"UPDATE users SET {update_clause} WHERE email = %s"
            cursor.execute(query, params)
            conn.commit()

            if cursor.rowcount == 0:
                return {"error": "User not found"}, 404

            return {"message": "User updated successfully"}
        except Exception as e:
            return {"error": str(e)}, 500
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def get_all_user_profiles():
        conn = User.get_db_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT role AS Role, description AS Description FROM user_profiles")
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def suspend_user_by_email(email):
        conn = User.get_db_connection()
        cursor = conn.cursor()

        query = "UPDATE users SET status = %s WHERE email = %s"
        cursor.execute(query, ("Suspended", email))
        conn.commit()
        affected = cursor.rowcount

        cursor.close()
        conn.close()

        if affected == 0:
            return {"error": "User not found"}, 404
        return {"message": f"User {email} suspended successfully."}




