from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from flask_mysql import MySQL
import jwt
import datetime
import uuid

app = Flask(__name__)
CORS(app)

app.config['MYSQL_HOST'] = 'your_mysql_host'
app.config['MYSQL_USER'] = 'your_mysql_user'
app.config['MYSQL_PASSWORD'] = 'your_mysql_password'
app.config['MYSQL_DB'] = 'your_mysql_db'

mysql = MySQL(app)
app.config['SECRET_KEY'] = 'your_secret_key'  # Change this to a secure, random key in production
app.config['REFRESH_SECRET_KEY'] = 'your_refresh_secret_key'  # Change this to another secure, random key

class User:
    def __init__(self, user_id, username, password, role):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.role = role

# Dummy user data
users = {
    1: User(1, 'admin', 'admin_password', 'admin'),
    2: User(2, 'user', 'user_password', 'user')
}

def generate_access_token(user_id, role):
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=15),  # Access token expiration time
        'iat': datetime.datetime.utcnow(),
        'sub': user_id,
        'role': role
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

def generate_refresh_token():
    return str(uuid.uuid4())

def verify_token(token, secret_key):
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return payload['sub'], payload['role']
    except jwt.ExpiredSignatureError:
        return 'Token has expired. Please log in again.', None
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.', None

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        # Perform authentication (replace this with your actual authentication logic)
        user = next((user for user in users.values() if user.username == username and user.password == password), None)

        if user:
            access_token = generate_access_token(user.user_id, user.role)
            refresh_token = generate_refresh_token()
            # Store the refresh token in your database associated with the user

            return jsonify({'success': True, 'access_token': access_token, 'refresh_token': refresh_token, 'role': user.role})

        return jsonify({'success': False, 'message': 'Invalid credentials'})

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/refresh', methods=['POST'])
def refresh():
    try:
        data = request.get_json()
        refresh_token = data.get('refresh_token')

        # Retrieve the user ID associated with the refresh token from your database
        # For simplicity, let's assume the user ID is 1 for now.
        user_id = 1

        # Retrieve the user's role from your database
        user = users.get(user_id)

        if user:
            access_token = generate_access_token(user_id, user.role)
            return jsonify({'success': True, 'access_token': access_token, 'role': user.role})

        return jsonify({'success': False, 'message': 'Invalid refresh token'})

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/protected', methods=['GET'])
def protected():
    try:
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'success': False, 'message': 'Token is missing'})

        user_id, user_role = verify_token(token, app.config['SECRET_KEY'])

        if isinstance(user_id, int) and user_role == 'admin':
            # Perform authorization logic for admin role
            return jsonify({'success': True, 'message': 'Admin access granted'})

        elif isinstance(user_id, int) and user_role == 'user':
            # Perform authorization logic for user role
            return jsonify({'success': True, 'message': 'User access granted'})

        return jsonify({'success': False, 'message': 'Access denied'})

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
