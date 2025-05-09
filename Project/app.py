import webbrowser
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import mysql.connector
from servicesCont import get_all_cleaners_with_services, search_cleaners, get_all_services
from favCont import get_favourite_cleaners

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
    if "user" not in session or session["user"]["role"] != "Cleaner":
        return redirect(url_for("login"))

    cleaner_id = session["user"]["id"]  # Make sure 'id' is in session["user"]

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT s.service_id, s.name, s.pricing, s.duration
        FROM service s
        JOIN cleaner_services cs ON s.service_id = cs.service_id
        WHERE cs.cleaner_id = %s
    """, (cleaner_id,))
    services = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template("dashboard_cleaner.html", services=services, cleaner_name=session["user"]["username"])

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
    cleaners = get_favourite_cleaners()
    return render_template('HOfav.html', favourites=cleaners)

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

@app.route('/get_cleaner_services', methods=['GET'])
def get_cleaner_services():
    cleaner_id = request.args.get('cleaner_id')  # Cleaner ID passed from the frontend

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

@app.route('/update_service/<int:service_id>', methods=['PUT'])
def update_service(service_id):
    data = request.json

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE service
        SET name = %s, pricing = %s, duration = %s
        WHERE service_id = %s
    """, (data['name'], data['pricing'], data['duration'], service_id))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'message': 'Service updated'})

@app.route('/delete_service/<int:service_id>', methods=['DELETE'])
def delete_service(service_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM service WHERE service_id = %s', (service_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Service deleted'})

@app.route("/services", methods=["GET"])
def get_all_services():
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

