import json
from flask import Flask
from flask import jsonify
from flask import request
from mongoengine import connect

from truck_requests import authenticate_incoming
from truck_requests import InvalidUsage
from models import Order
from lib.config import cfg

connect(name=cfg['db']['name'], host=cfg['db']['host'], port=cfg['db']['port'], connect=False)

app = Flask(__name__) 

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.route('/status')
def index():
    return jsonify(
        {
            "applicationName": "The Nimble Sloth Truck Simulator",
            "applicationAddress": cfg['api']['url'],
            "applicationStatus": "OK",
            "truckData": app.config['truck_data']._callmethod('__repr__')
        }
    )

@app.route('/orders')
def get_orders():

    # Authenticate warehouse is the requestor
    security_token = request.headers.get('X-Auth-Token')
    authenticate_incoming(app_id=cfg['requests']['warehouse_app_id'], token=security_token, session_id=app.config['session_id'])

    response = Order.objects
    actual_response = []
    for order in response:
        actual_response.append(
            {
                'order_id': order.order_id
            }
        )
    return jsonify({'status': 'ok', 'data': actual_response})
