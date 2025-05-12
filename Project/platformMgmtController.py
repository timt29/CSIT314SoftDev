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

class pltfMgmtController:
    def __init__(self, app, db_connector):
        self.app = app
        self.get_db_connection = db_connector
        self.register_routes()

