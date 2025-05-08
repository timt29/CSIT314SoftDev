from flask import Flask, request, jsonify, render_template, session, redirect
import json
import uuid
import os

useradminc = Flask(__name__)

useradminc.secret_key = "123"

user_files = 'user_db.json'
roles_files = 'role_db.json'

def load_users():
    
    if os.path.exists(user_files):
        with open(user_files, 'r') as f:
            return json.load(f)
    return []

def save_users(users):
    with open(user_files, 'w') as f:
        json.dump(users, f, indent = 4)

def load_roles():
    if os.path.exists(roles_files):
        with open(roles_files, 'r') as f:
            return json.load(f)
    return {}

def save_roles(roles):
    with open(roles_files, 'w') as f:
        json.dump(roles, f, indent = 4)