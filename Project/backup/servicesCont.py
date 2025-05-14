# from flask import request, render_template, session, jsonify, redirect
# import mysql.connector
# from typing import List, Dict

# def get_db_connection():
#     return mysql.connector.connect(
#         host="localhost",
#         user="root",
#         password="password",
#         database="testingcsit314"
#     )

# class ServiceController:
#     def __init__(self, app, db_connector):
#         self.app = app
#         self.get_db_connection = db_connector
#         self.register_routes()

#     def register_routes(self):
#         @self.app.route("/home")
#         def home():

#             user = session.get("user")
#             if not user:
#                 return redirect('/')

#             user_id = user.get("UserId")
#             conn = get_db_connection()
#             cursor = conn.cursor(dictionary=True)

#             cursor.execute("SELECT name FROM homeowner WHERE userid = %s", (user_id,))
#             homeowner = cursor.fetchone()

#             if not homeowner:
#                 return "homeowner not found", 404

#             cleaners = get_all_cleaners_with_services()
#             services = get_all_services()
#             return render_template(
#                 "HomeOwnerPg.html",
#                 cleaners=cleaners,
#                 services=services,
#                 search_query="",
#                 selected_service="",
#                 homeowner_name=homeowner["name"]
#             )

#         @self.app.route("/search", methods=["POST"])
#         def search():
            
#             user = session.get("user")
#             if not user:
#                 return redirect('/')

#             user_id = user.get("UserId")
#             conn = get_db_connection()
#             cursor = conn.cursor(dictionary=True)

#             cursor.execute("SELECT name FROM homeowner WHERE userid = %s", (user_id,))
#             homeowner = cursor.fetchone()

#             if not homeowner:
#                 return "homeowner not found", 404

#             search_query = request.form.get("search_query", "").strip()
#             selected_service = request.form.get("service_filter", "")
            
#             cleaners = search_cleaners(
#                 name_query=search_query if search_query else None,
#                 service_id=int(selected_service) if selected_service else None
#             )
            
#             services = get_all_services()
            
#             return render_template(
#                 "HomeOwnerPg.html",
#                 cleaners=cleaners,
#                 services=services,
#                 search_query=search_query,
#                 selected_service=selected_service,
#                 homeowner_name=homeowner["name"]
#             )
        
#         @self.app.route("/cleanerinfo")
#         def cleaner_info():
#             cleaner_id = request.args.get("cleaner_id", type=int)
#             service_id = request.args.get("service_id", type=int)

#             if not cleaner_id or not service_id:
#                 return "Cleaner ID and Service ID required", 400

#             conn = get_db_connection()
#             cursor = conn.cursor(dictionary=True)

#             # ✅ Increment view count only for the specific service
#             cursor.execute("""
#                 UPDATE cleanerservice 
#                 SET view_count = view_count + 1 
#                 WHERE userid = %s AND serviceid = %s
#             """, (cleaner_id, service_id))
#             conn.commit()

#             # ✅ Get cleaner name
#             cursor.execute("SELECT name FROM cleaner WHERE userid = %s", (cleaner_id,))
#             cleaner = cursor.fetchone()

#             # ✅ Get all services by the cleaner
#             cursor.execute("""
#                 SELECT s.serviceid, s.name, s.price, s.duration, cs.view_count
#                 FROM service s
#                 JOIN cleanerservice cs ON s.serviceid = cs.serviceid
#                 WHERE cs.userid = %s
#             """, (cleaner_id,))
#             services = cursor.fetchall()

#             cursor.close()
#             conn.close()

#             if not cleaner:
#                 return "Cleaner not found", 404

#             return render_template("cleanerinfo.html", cleaner_name=cleaner["name"], services=services, cleaner_id=cleaner_id)


#         @self.app.route("/api/book", methods=["POST"])
#         def api_book_service():
#             user = session.get("user")
#             if not user:
#                 return jsonify({"error": "Not logged in"}), 401

#             home_owner_id = user.get("UserId")
#             cleaner_id = request.json.get("cleaner_id")
#             service_id = request.json.get("service_id")
            
#             if not all([cleaner_id, service_id]):
#                 return jsonify({"error": "Missing fields"}), 400
            
#             try:
#                 conn = get_db_connection()
#                 cursor = conn.cursor()

#                 # Insert new booking into the booking table
#                 cursor.execute("""
#                     INSERT INTO booking (HomeOwnerId, CleanerId, ServiceId) 
#                     VALUES (%s, %s, %s)
#                 """, (home_owner_id, cleaner_id, service_id))
#                 conn.commit()

#                 # Check if the booking was successful
#                 if cursor.rowcount > 0:
#                     return jsonify({"message": "Booking successful!"}), 200
#                 else:
#                     return jsonify({"error": "Failed to book service"}), 500
                
#             except mysql.connector.Error as err:
#                 return jsonify({"error": f"Database error: {err}"}), 500

#             finally:
#                 cursor.close()
#                 conn.close()

#         @self.app.route("/services", methods=["GET"])
#         def fetch_all_services():
#             conn = get_db_connection()
#             cursor = conn.cursor(dictionary=True)
#             cursor.execute("SELECT * FROM service")
#             services = cursor.fetchall()
#             cursor.close()
#             conn.close()

#             return jsonify(services)

 
# def search_cleaners(name_query: str = None, service_id: int = None) -> List[Dict]:
#     """Search cleaners by name and/or service"""
#     try:
#         conn = mysql.connector.connect(
#             host="localhost",
#             user="root",
#             password="password",
#             database="testingcsit314",
#             port=3306,
#             auth_plugin='mysql_native_password'
#         )
#         cursor = conn.cursor(dictionary=True)
        
#         query = """
#         SELECT DISTINCT 
#         c.userid, 
#         c.name AS cleaner_name,
#         s.name AS service_name,
#         s.price,
#         s.duration
#         FROM cleaner c
#         JOIN cleanerservice cs ON c.UserId = cs.UserId
#         JOIN service s ON cs.ServiceId = s.ServiceId
#         WHERE 1=1
#         """
#         params = []
        
#         if name_query:
#             query += " AND c.name LIKE %s"
#             params.append(f"%{name_query}%")
            
#         if service_id:
#             query += " AND s.ServiceId = %s"
#             params.append(service_id)
            
#         query += " ORDER BY c.name ASC"
#         cursor.execute(query, tuple(params))
#         return cursor.fetchall()
        
#     except mysql.connector.Error as err:
#         print(f"MySQL Error: {err}")
#         return []
#     finally:
#         if 'conn' in locals() and conn.is_connected():
#             cursor.close()
#             conn.close()

# def get_all_services() -> List[Dict]:
#     """Get all available services"""
#     try:
#         conn = mysql.connector.connect(
#             host="localhost",
#             user="root",
#             password="password",
#             database="testingcsit314",
#             port=3306,
#             auth_plugin='mysql_native_password'
#         )
#         cursor = conn.cursor(dictionary=True)
#         cursor.execute("SELECT  serviceid, name  FROM service ORDER BY name")
#         return cursor.fetchall()
#     except mysql.connector.Error as err:
#         print(f"MySQL Error: {err}")
#         return []
#     finally:
#         if 'conn' in locals() and conn.is_connected():
#             cursor.close()
#             conn.close()



# def get_all_cleaners_with_services() -> List[Dict]:
    
#     """Get all cleaners with their service details"""
#     try:
#         conn = mysql.connector.connect(
#             host="localhost",
#             user="root",
#             password="password",
#             database="testingcsit314",
#             port=3306,
#             auth_plugin='mysql_native_password'
#         )
#         cursor = conn.cursor(dictionary=True)
        
#         query = """
#         SELECT 
#             c.userid,
#             c.name as cleaner_name,
#             s.serviceid,
#             s.name as service_name,
#             s.price,
#             s.duration,
#             CONCAT('$', s.price) as formatted_price
#         FROM cleaner c
#         LEFT JOIN cleanerservice cs ON c.UserId = cs.UserId
#         LEFT JOIN service s ON cs.serviceid = s.serviceid
#         ORDER BY c.name ASC
#         """
#         cursor.execute(query)
#         return cursor.fetchall()
        
#     except mysql.connector.Error as err:
#         print(f"MySQL Error: {err}")
#         return []
#     finally:
#         if 'conn' in locals() and conn.is_connected():
#             cursor.close()
#             conn.close()
