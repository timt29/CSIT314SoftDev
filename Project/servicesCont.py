import mysql.connector
from typing import List, Dict

def get_all_cleaners_with_services() -> List[Dict]:
    """Get all cleaners with their service details"""
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",
            database="testingcsit314",
            port=3306,
            auth_plugin='mysql_native_password'
        )
        cursor = conn.cursor(dictionary=True)
        
        query = """
        SELECT 
            c.userid,
            c.name as cleaner_name,
            s.serviceid,
            s.name as service_name,
            s.price,
            s.duration,
            CONCAT('$', s.price) as formatted_price
        FROM cleaner c
        LEFT JOIN cleanerservice cs ON c.UserId = cs.UserId
        LEFT JOIN service s ON cs.serviceid = s.serviceid
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
            database="testingcsit314",
            port=3306,
            auth_plugin='mysql_native_password'
        )
        cursor = conn.cursor(dictionary=True)
        
        query = """
        SELECT DISTINCT 
        c.userid, 
        c.name AS cleaner_name,
        s.name AS service_name,
        s.price,
        s.duration
        FROM cleaner c
        JOIN cleanerservice cs ON c.UserId = cs.UserId
        JOIN service s ON cs.ServiceId = s.ServiceId
        WHERE 1=1
        """
        params = []
        
        if name_query:
            query += " AND c.name LIKE %s"
            params.append(f"%{name_query}%")
            
        if service_id:
            query += " AND s.ServiceId = %s"
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
            database="testingcsit314",
            port=3306,
            auth_plugin='mysql_native_password'
        )
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT  serviceid, name  FROM service ORDER BY name")
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
        return []
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()