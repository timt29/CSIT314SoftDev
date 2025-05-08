import webbrowser
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import mysql.connector
from servicesCont import get_all_cleaners_with_services, search_cleaners, get_all_services

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Replace with a secure key

# MySQL connection function
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",  
        password="password", 
        database="csit314"
    )

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
                return redirect(url_for("admin_dashboard"))  # Correct endpoint name
            elif role == "Cleaner":
                return redirect(url_for("cleaner_dashboard"))  # Correct endpoint name
            elif role == "Home Owner":
                return redirect(url_for("home"))  # Correct endpoint name
            elif role == "Platform Management":
                return redirect(url_for("platform_dashboard"))  # Correct endpoint name
        else:
            return render_template("login.html", error="Invalid credentials or role")

    return render_template("login.html")

@app.route("/dashboard_admin")
def admin_dashboard():
    return render_template("dashboard_admin.html")

@app.route("/dashboard_cleaner")
def cleaner_dashboard():
    return render_template("dashboard_cleaner.html")

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

@app.route("/users", methods=["GET"])
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(users)

@app.route("/api/users", methods=["GET"])
def get_users_api():
    """Fetch all users from the database."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(users)

@app.route("/register", methods=["POST"])
def register_user():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users (email, password, username, role, dob, description)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        data["email"],
        data["password"],
        data["username"],
        data["role"],
        data["dob"],
        data["desc"]
    ))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "User registered"}), 201


if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:5000/")
    app.run(debug=True)

