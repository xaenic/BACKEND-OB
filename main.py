from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from dbhelper import *
import datetime
import uuid

app = Flask(__name__)
CORS(app)

# Load the secret key from the environment variable or use a default key
app.config['SECRET_KEY'] = '21312312'

# Setup Flask-JWT-Extended extension
jwt = JWTManager(app)

class User:
    def __init__(self, user_id, username, password, role):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.role = role

def generate_access_token(user_id, role,address):
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(days=7)
    payload = {
        'exp': expiration_time,
        'iat': datetime.datetime.utcnow(),
        'sub': user_id,
        'role': role,
        'address':address
    }
    return create_access_token(identity=payload)

def generate_refresh_token():
    return str(uuid.uuid4())

def verify_token(token, secret_key):
    try:
        payload = get_jwt_identity()
        return payload['sub'], payload['role']
    except Exception:
        return 'Invalid token. Please log in again.', None

@app.route('/admin/login', methods=['POST'])
def admin_login():
    try:
        data = request.get_json()
        print(data)
        username = data.get('username')
        password = data.get('password')
        print(username)
        if username == 'admin@gmail.com' and password == 'admin':
            print('yes')
            access_token = generate_access_token(1, 'admin')  # Assuming role is always 'admin' for simplicity
            refresh_token = generate_refresh_token()
            return jsonify({'success': True, 'access_token': access_token, 'refresh_token': refresh_token, 'role': 'admin'})
        return jsonify({'success': False, 'message': 'Invalid credentials'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        print(data)
        username = data.get('username')
        password = data.get('password')
        if username == 'admin@gmail.com' and password == 'admin':
            print('yes')
            access_token = generate_access_token(1, 'admin')  # Assuming role is always 'admin' for simplicity
            refresh_token = generate_refresh_token()
            return jsonify({'success': True, 'access_token': access_token, 'refresh_token': refresh_token, 'role': 'admin'})
        user = getuser('customers', email=username, password=password)
        if user:
            user = user[0]
            access_token = generate_access_token(user['id'], 'customer',user['address'])
            refresh_token = generate_refresh_token()
            return jsonify({'success': True, 'access_token': access_token, 'refresh_token': refresh_token, 'role': 'customer'})

        return jsonify({'success': False, 'message': 'Invalid credentials'})

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    try:
        user_id, user_role = verify_token(request.headers.get('Authorization'), app.config['SECRET_KEY'])

        if isinstance(user_id, int) and user_role == 'admin':
            return jsonify({'success': True, 'message': 'Admin access granted'})

        return jsonify({'success': False, 'message': 'Access denied'})

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})
@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/deletecart/<book_id>',methods=['GET'])
def delete_items_cart(book_id):
    ok = deleterecord('cart',book_id=book_id)
    resp = { 'status': ok}
    return jsonify(resp)
@app.route('/cartitems/<c_id>',methods=['GET'])
def getcart_items(c_id):
    c_id = int(c_id)
    ok = get_cart_items(c_id)
    resp = { 'status': 200,'results':  ok}
    return jsonify(resp)
@app.route('/cart',methods=['POST'])
def addto_cart():
    form_data = request.get_json()
    print(form_data)
    ok = addtocart('cart', **form_data)
    if ok:
        return {'status':True}
    return {'status':False}

@app.route('/get/<table>/<id>')
def get_data(table,id):
    ok = getrecord(table.lower(),id=int(id))
    resp = { 'status': 200, 'results':  ok}
    return jsonify(resp)
@app.route('/<table>/<page>/<limit>')
def customers(table,page,limit):

    ok = getall(table.lower(),int(page),int(limit))
    resp = { 'status': 200,'page':page, 'results':  ok}
    return jsonify(resp)
@app.route('/search/<type>/<key>')
def search(type,key):
    resp = { 'status': 200, 'results': searchK(type.lower(),key) }

    return jsonify(resp)



@app.route('/items/<o_id>')
def items(o_id):
    resp = {
        'status': 200,
        'results': getItems(int(o_id))
    }

    return jsonify(resp)
@app.route('/orders/<id>')
def orders(id):
    resp = { 'status': 200,
        'results': getOrders(int(id)) }
    return jsonify(resp)

@app.route('/create/<table>',methods=['POST'])
def asdaw(table):
    form_data = request.get_json()
    

    resp = { 'status': 200,
        'results': addrecord(table.lower(),**form_data) }
    return jsonify(resp)
@app.route('/edit/<table>/<id>',methods=['POST'])
def edit(table,id):
    form_data = request.get_json()
    
    resp = { 'status': 200,
        'results': updaterecord(table.lower(),id=id,**form_data) }
    return jsonify(resp)

@app.route('/placeorder',methods=['POST'])
def place_order():
    form_data = request.get_json()
    ok = placeorder(form_data['c_id'],form_data['items'],form_data['address'])
    return {'status':ok}
@app.route('/test')
def asdd():
    delete('ordered_items',c_id=1)
    return 'test'
@app.route('/delete/<table>/<id>')
def asd(table,id):
    delete('ordered_items',c_id=int(id))
    deleterecord('orders',c_id=int(id))
    deleterecord('cart',c_id=int(id))
    deleterecord('reviews',c_id=int(id))
    if 'items' in table.lower():
        deleterecord('ordered_items', i_id=int(id))
    resp = { 'status': 200,
        'results': deleterecord(table.lower(),id=int(id)) }
    return jsonify(resp)

@app.route('/reviews/<id>')
def reviews(id):
    
    resp = {
        'status': 200,
        'results': getReviews(id)
    }

    return jsonify(resp)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)
