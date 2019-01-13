import json
from flask import Flask
from flask import jsonify
from mongoengine import connect

from models import Order
from lib.config import cfg

connect(name=cfg['db']['name'], host=cfg['db']['host'], port=cfg['db']['port'], connect=False)

app = Flask(__name__)

@app.route('/status')
def index():
    return jsonify(
        {
            "applicationName": "The Nimble Sloth Truck Simulator",
            "applicationAddress": cfg['api']['url'],
            "applicationStatus": "OK"
        }
    )

@app.route('/orders')
def get_orders():
    response = Order.objects
    actual_response = []
    for order in response:
        actual_response.append(
            {
                'order_id': order.order_id
            }
        )
    return jsonify({'status': 'ok', 'data': actual_response})
