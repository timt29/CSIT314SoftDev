import mysql.connector

class UserProfile:
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
    def get_user_profiles(search_query=None):
        conn = UserProfile.get_db_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            if search_query:
                cursor.execute("""
                    SELECT * FROM UserProfile
                    WHERE Role LIKE %s OR Description LIKE %s
                """, (f"%{search_query}%", f"%{search_query}%"))
            else:
                cursor.execute("SELECT * FROM UserProfile")
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def create_profile(role, description):
        conn = UserProfile.get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO UserProfile (Role, Description) VALUES (%s, %s)",
                (role, description)
            )
            conn.commit()
            return {"message": "User profile created successfully"}, 201
        except mysql.connector.IntegrityError:
            return {"error": "Role already exists"}, 409
        except Exception as e:
            return {"error": str(e)}, 500
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def update_profile_description(role, description):
        conn = UserProfile.get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE UserProfile SET Description = %s WHERE Role = %s",
                (description, role)
            )
            conn.commit()
            if cursor.rowcount == 0:
                return {"error": "Role not found"}, 404
            return {"message": "Description updated successfully"}, 200
        except Exception as e:
            return {"error": str(e)}, 500
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def delete_by_role(role):
        conn = UserProfile.get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM UserProfile WHERE Role = %s", (role,))
            conn.commit()
            if cursor.rowcount == 0:
                return {"error": "Role not found"}, 404
            return {"message": "User profile deleted successfully"}, 200
        except Exception as e:
            return {"error": str(e)}, 500
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def search(query):
        conn = UserProfile.get_db_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            if query:
                cursor.execute("""
                    SELECT * FROM UserProfile
                    WHERE Role LIKE %s OR Description LIKE %s
                """, (f"%{query}%", f"%{query}%"))
            else:
                cursor.execute("SELECT * FROM UserProfile")
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()