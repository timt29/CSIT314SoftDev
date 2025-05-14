import webbrowser
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import mysql.connector
from UserProfileController import UserProfileController
from UserAdminController import login_controller
from servicesCont import ServiceController
from favCont import FavouriteController
from historyCont import HistoryController
from CleanerController import CleanerController
from platformMgmtController import pltfMgmtController
from ViewUserController import ViewUserController
from ViewUserBoundary import register_routes
from User import User

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
#AdminController(app, get_db_connection)
UserProfileController(app, get_db_connection)
login_controller(app)
CleanerController(app, get_db_connection)
ServiceController(app, get_db_connection)
FavouriteController(app, get_db_connection)
HistoryController(app, get_db_connection)
pltfMgmtController(app, get_db_connection)
ViewUserController()
register_routes(app)
User(get_db_connection)

@app.route("/dashboard_platform")
def platform_dashboard():
    return render_template("dashboard_platform.html")

if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:5000/")
    app.run(debug=True)

