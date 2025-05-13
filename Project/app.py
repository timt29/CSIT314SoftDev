import webbrowser
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import mysql.connector
from servicesCont import get_all_cleaners_with_services, search_cleaners, get_all_services
from favCont import get_favourite_cleaners
from historyCont import get_service_history
from UserProfileController import UserProfileController
from UserAdminController import AdminController, login_controller
from CleanerController import CleanerController
from platformMgmtController import pltfMgmtController

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Replace with a secure key

# MySQL connection function
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",  
        password="password", 
        database="testingcsit314"
    )

# Initialize Controllers
AdminController(app, get_db_connection)
UserProfileController(app, get_db_connection)
login_controller(app)
CleanerController(app, get_db_connection)

@app.route("/dashboard_platform")
def platform_dashboard():
    return render_template("dashboard_platform.html")


@app.route("/cleanerinfo")
def cleaner_info():
    cleaner_id = request.args.get("cleaner_id", type=int)
    service_id = request.args.get("service_id", type=int)

    if not cleaner_id or not service_id:
        return "Cleaner ID and Service ID required", 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # ✅ Increment view count only for the specific service
    cursor.execute("""
        UPDATE cleanerservice 
        SET view_count = view_count + 1 
        WHERE userid = %s AND serviceid = %s
    """, (cleaner_id, service_id))
    conn.commit()

    # ✅ Get cleaner name
    cursor.execute("SELECT name FROM cleaner WHERE userid = %s", (cleaner_id,))
    cleaner = cursor.fetchone()

    # ✅ Get all services by the cleaner
    cursor.execute("""
        SELECT s.serviceid, s.name, s.price, s.duration, cs.view_count
        FROM service s
        JOIN cleanerservice cs ON s.serviceid = cs.serviceid
        WHERE cs.userid = %s
    """, (cleaner_id,))
    services = cursor.fetchall()

    cursor.close()
    conn.close()

    if not cleaner:
        return "Cleaner not found", 404

    return render_template("cleanerinfo.html", cleaner_name=cleaner["name"], services=services, cleaner_id=cleaner_id)


@app.route("/home")
def home():

    user = session.get("user")
    if not user:
        return redirect('/')

    user_id = user.get("UserId")
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT name FROM homeowner WHERE userid = %s", (user_id,))
    homeowner = cursor.fetchone()

    if not homeowner:
        return "homeowner not found", 404

    cleaners = get_all_cleaners_with_services()
    services = get_all_services()
    return render_template(
        "HomeOwnerPg.html",
        cleaners=cleaners,
        services=services,
        search_query="",
        selected_service="",
        homeowner_name=homeowner["name"]
    )

@app.route("/search", methods=["POST"])
def search():
    
    user = session.get("user")
    if not user:
        return redirect('/')

    user_id = user.get("UserId")
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT name FROM homeowner WHERE userid = %s", (user_id,))
    homeowner = cursor.fetchone()

    if not homeowner:
        return "homeowner not found", 404

    search_query = request.form.get("search_query", "").strip()
    selected_service = request.form.get("service_filter", "")
    
    cleaners = search_cleaners(
        name_query=search_query if search_query else None,
        service_id=int(selected_service) if selected_service else None
    )
    
    services = get_all_services()
    
    return render_template(
        "HomeOwnerPg.html",
        cleaners=cleaners,
        services=services,
        search_query=search_query,
        selected_service=selected_service,
        homeowner_name=homeowner["name"]

    )

@app.route('/fav')
def favourites_page():
    user = session.get("user")
    if not user:
        return redirect('/')

    user_id = user.get("UserId")
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT name FROM homeowner WHERE userid = %s", (user_id,))
    homeowner = cursor.fetchone()

    if not homeowner:
        return "homeowner not found", 404
    cleaners = get_favourite_cleaners(user_id)
    return render_template(
        'HOfav.html',
        favourites=cleaners,
        homeowner_name=homeowner["name"])

@app.route("/history")
def view_history():
    user = session.get("user")
    if not user:
        return redirect('/')

    user_id = user.get("UserId")
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT name FROM homeowner WHERE userid = %s", (user_id,))
    homeowner = cursor.fetchone()

    if not homeowner:
        return "homeowner not found", 404
    from servicesCont import get_all_services

    service_id = request.args.get("service_filter", type=int)
    date_used = request.args.get("date_used")

    history = get_service_history(service_id, date_used)
    services = get_all_services()

    return render_template(
        "history.html",
        history=history,
        services=services,
        selected_service=service_id,
        date_used=date_used or "",
        homeowner_name=homeowner["name"]
    )

@app.route("/services", methods=["GET"])
def fetch_all_services():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM service")
    services = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(services)

@app.route("/api/book", methods=["POST"])
def api_book_service():
    user = session.get("user")
    if not user:
        return jsonify({"error": "Not logged in"}), 401

    home_owner_id = user.get("UserId")
    cleaner_id = request.json.get("cleaner_id")
    service_id = request.json.get("service_id")
    
    if not all([cleaner_id, service_id]):
        return jsonify({"error": "Missing fields"}), 400
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Insert new booking into the booking table
        cursor.execute("""
            INSERT INTO booking (HomeOwnerId, CleanerId, ServiceId) 
            VALUES (%s, %s, %s)
        """, (home_owner_id, cleaner_id, service_id))
        conn.commit()

        # Check if the booking was successful
        if cursor.rowcount > 0:
            return jsonify({"message": "Booking successful!"}), 200
        else:
            return jsonify({"error": "Failed to book service"}), 500
        
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500

    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:5000/")
    app.run(debug=True)

