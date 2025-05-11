from flask import render_template
import mysql.connector

# Utility function for database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="testingcsit314"
    )

@app.route('/dashboard')
def dashboard():
    username = "JohnDoe"  # Replace with the actual logged-in username
    return render_template('dashboard_platform.html', username=username)