from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

@app.route('/get_cleaner_services', methods=['GET'])
def get_cleaner_services():
    userid = request.args.get('userid')

    # Connect to your database
    db = mysql.connector.connect(
        host="localhost",
        user="your_mysql_user",
        password="your_mysql_password",
        database="csit314"
    )
    cursor = db.cursor(dictionary=True)

    # Get service names for the cleaner
    query = """
        SELECT s.name AS service_name
        FROM cleaner_service cs
        JOIN service s ON cs.service_id = s.service_id
        WHERE cs.userid = %s
    """
    cursor.execute(query, (userid,))
    services = cursor.fetchall()

    cursor.close()
    db.close()

    return jsonify(services)

if __name__ == '__main__':
    app.run(debug=True)