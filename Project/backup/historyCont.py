# from flask import request, render_template, session, jsonify, redirect
# import mysql.connector

# def get_db_connection():
#     return mysql.connector.connect(
#         host="localhost",
#         user="root",
#         password="password",
#         database="testingcsit314"
#     )

# class HistoryController:
#     def __init__(self, app, db_connector):
#         self.app = app
#         self.get_db_connection = db_connector
#         self.register_routes()

#     def register_routes(self):

#         @self.app.route("/history")
#         def view_history():
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
#             from Project.backup.servicesCont import get_all_services

#             service_id = request.args.get("service_filter", type=int)
#             date_used = request.args.get("date_used")

#             history = get_service_history(service_id, date_used)
#             services = get_all_services()

#             return render_template(
#                 "history.html",
#                 history=history,
#                 services=services,
#                 selected_service=service_id,
#                 date_used=date_used or "",
#                 homeowner_name=homeowner["name"]
#             )

# def get_service_history(service_id=None, date_used=None):
#     try:
#         user = session.get("user")
#         if not user:
#             return []

#         homeowner_id = user.get("UserId")

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
#             h.date_used, 
#             c.name AS cleaner_name, 
#             s.name AS service_name, 
#             s.price
#         FROM history h
#         JOIN cleaner c ON h.cleanerid = c.userid
#         JOIN service s ON h.serviceid = s.serviceid
#         WHERE h.homeownerid = %s
#         """
#         params = [homeowner_id]
#         if service_id:
#             query += " AND s.serviceid = %s"
#             params.append(service_id)

#         if date_used:
#             query += " AND DATE(h.date_used) = %s"
#             params.append(date_used)

#         query += " ORDER BY h.date_used DESC"
#         cursor.execute(query, params)
#         return cursor.fetchall()

#     except mysql.connector.Error as err:
#         print(f"MySQL Error: {err}")
#         return []
#     finally:
#         if 'conn' in locals() and conn.is_connected():
#             cursor.close()
#             conn.close()
