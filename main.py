from flask import Flask,jsonify,request
import json
from flask_cors import CORS
from dbhelper import *
from urllib.parse import parse_qs
app = Flask(__name__)
CORS(app)
@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/get/<table>/<id>')
def wss(table,id):
    ok = getrecord(table,id=int(id))
    resp = { 'status': 200, 'results':  ok}
    return jsonify(resp)
@app.route('/<table>/<page>')
def customers(table,page):

    ok = getall(table,int(page))
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
        'results': addrecord(table,**form_data) }
    return jsonify(resp)
@app.route('/edit/<table>/<id>',methods=['POST'])
def edit(table,id):
    form_data = request.get_json()
    
    resp = { 'status': 200,
        'results': updaterecord(table,id=id,**form_data) }
    return jsonify(resp)
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
    resp = { 'status': 200,
        'results': deleterecord(table,id=int(id)) }
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
