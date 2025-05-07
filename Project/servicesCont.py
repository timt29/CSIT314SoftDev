import mysql.connector
from typing import List, Dict

def get_all_cleaners_with_services() -> List[Dict]:
    """Get all cleaners with their service details"""
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",
            database="csit314",
            port=3306,
            auth_plugin='mysql_native_password'
        )
        cursor = conn.cursor(dictionary=True)
        
        query = """
        SELECT 
            c.userid,
            c.name as cleaner_name,
            c.experience,
            s.name as service_name,
            s.pricing,
            s.duration,
            CONCAT('$', s.pricing) as formatted_price
        FROM cleaner c
        JOIN service s ON c.service_id = s.service_id
        ORDER BY c.name ASC
        """
        cursor.execute(query)
        return cursor.fetchall()
        
    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
        return []
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

def search_cleaners(name_query: str = None, service_id: int = None) -> List[Dict]:
    """Search cleaners by name and/or service"""
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",
            database="csit314",
            port=3306,
            auth_plugin='mysql_native_password'
        )
        cursor = conn.cursor(dictionary=True)
        
        query = """
        SELECT 
            c.userid,
            c.name as cleaner_name,
            c.experience,
            s.name as service_name,
            s.pricing,
            s.duration,
            CONCAT('$', s.pricing) as formatted_price
        FROM cleaner c
        JOIN service s ON c.service_id = s.service_id
        WHERE 1=1
        """
        params = []
        
        if name_query:
            query += " AND c.name LIKE %s"
            params.append(f"%{name_query}%")
            
        if service_id:
            query += " AND s.service_id = %s"
            params.append(service_id)
            
        query += " ORDER BY c.name ASC"
        cursor.execute(query, tuple(params))
        return cursor.fetchall()
        
    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
        return []
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

def get_all_services() -> List[Dict]:
    """Get all available services"""
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",
            database="csit314",
            port=3306,
            auth_plugin='mysql_native_password'
        )
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM service ORDER BY name")
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
        return []
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()