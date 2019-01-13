import json
from flask import Flask
from mongoengine import connect

from models import Order
from lib.config import cfg

connect(name=cfg['db']['name'], host=cfg['db']['host'], port=cfg['db']['port'], connect=False)

app = Flask(__name__)

@app.route('/status')
def index():
    return json.dumps({'status': 'ok', 'data': {}})

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
    return json.dumps({'status': 'ok', 'data': actual_response})
