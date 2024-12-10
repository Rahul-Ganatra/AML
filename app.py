from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS
import os
import firebase_admin
from firebase_admin import credentials, auth

app = Flask(__name__)
CORS(app)

# Initialize Firebase Admin
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

# Route to serve static files
@app.route('/<path:path>')
def serve_file(path):
    if path == "":
        return send_from_directory('.', 'index.html')
    return send_from_directory('.', path)

# Root route
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# Login API endpoint
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')
    
    try:
        # Verify with Firebase Auth
        user = auth.get_user_by_email(email)
        return jsonify({"status": "success", "role": role})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# Signup API endpoint
@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')
    
    try:
        # Create user in Firebase Auth
        user = auth.create_user(
            email=email,
            password=password
        )
        return jsonify({"status": "success", "role": role})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
