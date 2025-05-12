import webbrowser
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import mysql.connector
from servicesCont import get_all_cleaners_with_services, search_cleaners, get_all_services
from favCont import get_favourite_cleaners
from historyCont import get_service_history
from UserProfileController import UserProfileController
from UserAdminController import AdminController, login_controller
from CleanerController import CleanerController

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


'''@app.route("/cleanerinfo")
def cleaner_info():
            user = session.get("user")
            if not user:
                return redirect('/')

            user_id = user.get("UserId")
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute("SELECT name FROM cleaner WHERE userid = %s", (user_id,))
            cleaner = cursor.fetchone()

            cursor.execute("""
                SELECT s.serviceid, s.name, s.price, s.duration
                FROM service s
                JOIN cleanerservice cs ON s.serviceid = cs.serviceid
                WHERE cs.userid = %s
            """, (user_id,))
            services = cursor.fetchall()

            cursor.close()
            conn.close()

            if not cleaner:
                return "Cleaner not found", 404

            return render_template("cleanerinfo.html", cleaner_name=cleaner["name"], services=services)'''

@app.route("/cleanerinfo")
def cleaner_info():
    # Hardcoding the user_id as 6
    user_id = 6  # Directly set to 6 to simulate login

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Query for cleaner info based on hardcoded user_id (6)
    cursor.execute("SELECT name FROM cleaner WHERE userid = %s", (user_id,))
    cleaner = cursor.fetchone()

    # Query for services provided by this cleaner
    cursor.execute("""
        SELECT s.serviceid, s.name, s.price, s.duration
        FROM service s
        JOIN cleanerservice cs ON s.serviceid = cs.serviceid
        WHERE cs.userid = %s
    """, (user_id,))
    services = cursor.fetchall()

    cursor.close()
    conn.close()

    if not cleaner:
        return "Cleaner not found", 404

    return render_template("cleanerinfo.html", cleaner_name=cleaner["name"], services=services)

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
    session["homeowner_id"] = 4  # Force-set for testing
    cleaners = get_favourite_cleaners()
    return render_template('HOfav.html', favourites=cleaners)

@app.route("/history")
def view_history():
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
        date_used=date_used or ""
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

@app.route("/book_service", methods=["POST"])
def book_service():
    # Get the service_id from the POST data
    data = request.get_json()  # Expecting JSON body in the request
    
    service_id = data.get('service_id')
    homeowner_id = session.get('homeowner_id')  # Assuming homeowner ID is stored in the session
    cleaner_id = data.get('cleaner_id')  # The cleaner that the homeowner is booking
    
    if not service_id or not homeowner_id or not cleaner_id:
        return jsonify({"message": "Missing required information!"}), 400

    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Insert booking into the database
        query = """
            INSERT INTO bookings (homeowner_id, service_id, cleaner_id, booking_date)
            VALUES (%s, %s, %s, NOW())
        """
        cursor.execute(query, (homeowner_id, service_id, cleaner_id))
        conn.commit()  # Commit the transaction

        # Optionally, you can fetch the booking ID or any other info you need
        # booking_id = cursor.lastrowid

        return jsonify({"message": "Service has been booked successfully!"}), 200
    except Exception as e:
        conn.rollback()  # If there was an error, rollback the transaction
        return jsonify({"message": f"Error booking service: {str(e)}"}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:5000/")
    app.run(debug=True)

