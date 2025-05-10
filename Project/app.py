import webbrowser
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import mysql.connector
from servicesCont import get_all_cleaners_with_services, search_cleaners, get_all_services
from favCont import get_favourite_cleaners
from historyCont import get_service_history
from UserProfileController import UserProfileController
from UserAdminController import AdminController

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

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM users WHERE email = %s AND password = %s AND role = %s",
            (email, password, role)
        )
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            session["user"] = user
            if role == "Admin User":
                return redirect(url_for("admin_dashboard"))  # Handled by AdminController
            elif role == "Cleaner":
                return redirect(url_for("cleaner_dashboard"))
            elif role == "Home Owner":
                return redirect(url_for("home"))
            elif role == "Platform Management":
                return redirect(url_for("platform_dashboard"))
        else:
            return render_template("login.html", error="Invalid credentials or role")

    return render_template("login.html")

@app.route("/dashboard_cleaner")
def cleaner_dashboard():
    user = session.get("user")
    if not user:
        return redirect('/login')  # Redirect to login if not logged in

    user_id = user.get("id")  # Extract the user ID from session

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Get the cleaner's info
    cursor.execute("SELECT name FROM cleaner WHERE userid = %s", (user_id,))
    cleaner = cursor.fetchone()

    # Get services assigned to the cleaner
    cursor.execute("""
        SELECT s.name AS service_name, s.pricing, s.duration 
        FROM service s
        JOIN cleaner_services cs ON s.service_id = cs.service_id
        WHERE cs.cleaner_id = %s
    """, (user_id,))
    services = cursor.fetchall()

    cursor.close()
    conn.close()

    if not cleaner:
        return "Cleaner not found!"

    return render_template('dashboard_cleaner.html', cleaner_name=cleaner['name'], services=services)

@app.route("/dashboard_platform")
def platform_dashboard():
    return render_template("dashboard_platform.html")

@app.route("/home")
def home():
    cleaners = get_all_cleaners_with_services()
    services = get_all_services()
    return render_template(
        "HomeOwnerPg.html",
        cleaners=cleaners,
        services=services,
        search_query="",
        selected_service=""
    )

@app.route("/search", methods=["POST"])
def search():
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
        selected_service=selected_service
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



@app.route("/get_cleaner_services", methods=["GET"])
def get_cleaner_services():
    cleaner_id = session.get("user", {}).get("id")
    if not cleaner_id:
        return jsonify({"error": "User not logged in"}), 401
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT s.service_id, s.name, s.pricing, s.duration
        FROM service s
        JOIN cleaner_services cs ON s.service_id = cs.service_id
        WHERE cs.cleaner_id = %s
    """, (cleaner_id,))
    cleaner_services = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(cleaner_services)

@app.route('/add_service', methods=['POST'])
def add_service():
    user = session.get("user")
    if not user:
        return jsonify({"error": "User not logged in"}), 401

    data = request.json
    name = data.get("name")
    pricing = data.get("pricing")
    duration = data.get("duration")

    # Find the cleaner_id from user_id
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT cleaner_id FROM cleaner WHERE userid = %s", (user["id"],))
    result = cursor.fetchone()
    if not result:
        return jsonify({"error": "Cleaner not found"}), 404

    cleaner_id = result[0]

    # Insert into service table
    cursor.execute("""
        INSERT INTO service (name, pricing, duration)
        VALUES (%s, %s, %s)
    """, (name, pricing, duration))
    service_id = cursor.lastrowid

    # Link service to cleaner
    cursor.execute("""
        INSERT INTO cleaner_services (cleaner_id, service_id)
        VALUES (%s, %s)
    """, (cleaner_id, service_id))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Service added successfully"})

@app.route("/services", methods=["GET"])
def fetch_all_services():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM service")
    services = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(services)

if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:5000/")
    app.run(debug=True)

