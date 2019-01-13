import pika
import time
import json
from mongoengine import connect

from lib.config import cfg
from models import Order

def callback(ch, method, properties, body, truck_data):
    print 'Received new order'
    orders = json.loads(body)
    for order in orders:
        db_order = Order(order_id=order['orderId'], 
                            dest_lat=order['destination']['latitude'], 
                            dest_lng=order['destination']['longitude']).save()
        print 'Order saved in db'
    truck_data['status'] = 'ON_THE_ROAD_AGAIN'
    time.sleep(20)
    truck_data['status'] = 'CHILLIN_IN_WAREHOUSE'
    #TODO update statuses, ask for recipient data


def subscribe(session_id, truck_data):
    connect(name=cfg['db']['name'], host=cfg['db']['host'], port=cfg['db']['port'], connect=False)
    connection = pika.BlockingConnection(pika.URLParameters(cfg['rabbit']['url']))
    channel = connection.channel()

    channel.queue_declare(queue=cfg['rabbit']['queue'], durable=True)
    channel.basic_consume(lambda ch, method, properties, body: callback(ch, method, properties, body, truck_data),
                        queue=cfg['rabbit']['queue'],
                        no_ack=True)

    print 'Started listening to the queue'
    channel.start_consuming()

if __name__ == '__main__':
    subscribe()