import webbrowser
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import mysql.connector
#from UserProfileController import UserProfileController
#from UserAdminController import login_controller
from CleanerServicesBoundary import register_routes2
from HistoryBoundary import register_routes3
from FavouriteBoundary import register_routes4 
from User import User
from ServiceBoundary import register_routes5
from ViewServiceController import ViewServiceController
from CreateServiceController import CreateServiceController
from UpdateServiceController import UpdateServiceController
from DeleteServiceController import DeleteServiceController
from SearchServiceController import SearchServiceController
from Service import Service
from ViewCountController import ViewCountController
from ViewShortlistController import ViewShortlistController
from Number import Number
from BookingBoundary import register_routes6
from ViewBookingController import ViewBookingController
from SearchBookingController import SearchBookingController
from Booking import Booking
from PlatformManagementController import PlatformManagementController
from PlatformManagementBoundary import register_routes7
#User & UserProfile
from LoginBoundary import register_login_routes
from LogoutBoundary import register_routes as logout_routes
from UserBoundary import register_user_routes as user_routes
from UserProfileBoundary import register_profile_routes as profile_routes

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
#UserProfileController(app, get_db_connection)
#login_controller(app)
#pltfMgmtController(app, get_db_connection)
#ViewUserController()
#register_routes(app)
register_routes2(app)
register_routes3(app)
register_routes4(app) 
register_routes5(app)
register_routes6(app)
register_routes7(app)
ViewServiceController()
CreateServiceController()
UpdateServiceController()
DeleteServiceController()
SearchServiceController()
Service(get_db_connection)
ViewCountController()
ViewShortlistController()
Number(get_db_connection)
ViewBookingController()
SearchBookingController()
Booking(get_db_connection)
PlatformManagementController()
#User & UserProfile
user_routes(app)
register_login_routes(app)
logout_routes(app)
profile_routes(app)

@app.route("/dashboard_platform")
def platform_dashboard():
    return render_template("dashboard_platform.html")

if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:5000/")
    app.run(debug=False)

