import webbrowser
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import mysql.connector
from favCont import get_favourite_cleaners
from historyCont import get_service_history
from UserProfileController import UserProfileController
from UserAdminController import AdminController, login_controller
from servicesCont import ServiceController
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
ServiceController(app, get_db_connection)

@app.route("/dashboard_platform")
def platform_dashboard():
    return render_template("dashboard_platform.html")

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



if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:5000/")
    app.run(debug=True)

