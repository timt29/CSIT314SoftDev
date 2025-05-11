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

