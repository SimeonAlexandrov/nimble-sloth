import pika
import time
import json
from mongoengine import connect

from constants import CONSTANTS
from lib.config import cfg
from models import Order
from api.truck_requests import update_order_status
from api.truck_requests import warehouse_put
from api.truck_requests import warehouse_delete
from api.truck_requests import get_receiver_info


def are_orders_from_warehouse_to_address(orders):
    first_lat = orders[0]['pickUp']['latitude']
    first_lng = orders[0]['pickUp']['longitude']

    return first_lat ==  CONSTANTS['WAREHOUSE_LOCATION']['LAT'] and \
                                first_lng ==  CONSTANTS['WAREHOUSE_LOCATION']['LNG']


def callback(ch, method, properties, body, truck_data, session_id):
    try: 

        print 'Received new orders'
        orders = json.loads(body)

        if are_orders_from_warehouse_to_address(orders):
            truck_data['status'] = CONSTANTS['TRUCK']['DELIVERING_ORDER']
        else:
            truck_data['status'] = CONSTANTS['TRUCK']['TRAVELLING_TO_WAREHOUSE']

        for order in orders:
            if are_orders_from_warehouse_to_address(orders):
                # Pop from warehouse
                warehouse_delete(order['orderId'], session_id)
            
            receiver_info = get_receiver_info(order['orderId'])

            db_order = Order(order_id=order['orderId'], 
                                dest_lat=order['destination']['latitude'], 
                                dest_lng=order['destination']['longitude'],
                                src_lat=order['pickUp']['latitude'],
                                src_lng=order['pickUp']['longitude'],
                                status=CONSTANTS['ORDER']['DELIVERING']).save()
            
            print 'Order saved in db'

            update_order_status(CONSTANTS['ORDER']['DELIVERING'], order['orderId'])
        
        for order in orders:
                    
            time.sleep(10)
            if are_orders_from_warehouse_to_address(orders):
                update_order_status(CONSTANTS['ORDER']['DELIVERED'], order['orderId'])
                # Update in local db
                print 'Order {} is delivered {}'.format(order['orderId'], 'AT_RECEIVER_ADDRESS')
            else:
                # warehouse_put(order, session_id)
                update_order_status(CONSTANTS['ORDER']['AT_WAREHOUSE'], order['orderId'])
                # Update in local db
                print 'Order {} is delivered {}'.format(order['orderId'], 'AT_WAREHOUSE')

        if are_orders_from_warehouse_to_address(orders):
            truck_data['status'] = CONSTANTS['TRUCK']['TRAVELLING_TO_WAREHOUSE']
            time.sleep(10)
        truck_data['status'] = CONSTANTS['TRUCK']['AT_WAREHOUSE']
        print 'ok'
    except Exception as e:
        print 'Something went wrong with queue callback'
        print e

def subscribe(session_id, truck_data):
    connect(name=cfg['db']['name'], host=cfg['db']['host'], port=cfg['db']['port'], connect=False)
    connection = pika.BlockingConnection(pika.URLParameters(cfg['rabbit']['url']))
    channel = connection.channel()

    channel.queue_declare(queue=cfg['rabbit']['queue'], durable=True)
    channel.basic_consume(lambda ch, method, properties, body: callback(ch, method, properties, body, truck_data, session_id),
                        queue=cfg['rabbit']['queue'],
                        no_ack=True)

    print 'Started listening to the queue'
    channel.start_consuming()

if __name__ == '__main__':
    subscribe()