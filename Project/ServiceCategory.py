import mysql.connector

class ServiceCategory:
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
    def get_service_category(search_query=None):
        conn = ServiceCategory.get_db_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            if search_query:
                cursor.execute("""
                    SELECT * FROM ServiceCategory
                    WHERE CategoryName LIKE %s
                """, (f"%{search_query}%",))
            else:
                cursor.execute("SELECT * FROM ServiceCategory")
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def createServiceCategory(CategoryName):
        conn = ServiceCategory.get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO ServiceCategory (CategoryName) VALUES (%s)",
                (CategoryName)
            )
            conn.commit()
            return {"message": "Service Category created successfully"}, 201
        except mysql.connector.IntegrityError:
            return {"error": "Category already exists"}, 409
        except Exception as e:
            return {"error": str(e)}, 500
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def updateServiceCategory(CategoryName):
        conn = ServiceCategory.get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE ServiceCategory SET CategoryName = %s",
                (CategoryName)
            )
            conn.commit()
            if cursor.rowcount == 0:
                return {"error": "Category not found"}, 404
            return {"message": "Category updated successfully"}, 200
        except Exception as e:
            return {"error": str(e)}, 500
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def deleteServiceCategory(CategoryName):
        conn = ServiceCategory.get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM ServiceCategory WHERE CategoryName = %s", (CategoryName,))
            conn.commit()
            if cursor.rowcount == 0:
                return {"error": "Category not found"}, 404
            return {"message": "Service Category deleted successfully"}, 200
        except Exception as e:
            return {"error": str(e)}, 500
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def searchcategory(query):
        conn = ServiceCategory.get_db_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            if query:
                cursor.execute("""
                    SELECT * FROM ServiceCategory
                    WHERE CategoryName LIKE %s
                """, (f"%{query}%",))
            else:
                cursor.execute("SELECT * FROM ServiceCategory")
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()