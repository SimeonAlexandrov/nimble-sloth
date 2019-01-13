import pika
import json
from mongoengine import connect

from lib.config import cfg
from models import Order

def callback(ch, method, properties, body):
    print 'Received new order'
    order = json.loads(body)
    db_order = Order(order_id=order['order_id'], dest_lat=order['dest_lat'], dest_lng=order['dest_lng']).save()
    #TODO update statuses, ask for recipient data


def subscribe(session_id):
    connect(name=cfg['db']['name'], host=cfg['db']['host'], port=cfg['db']['port'], connect=False)
    connection = pika.BlockingConnection(pika.URLParameters('amqp://xnennbql:uu7tKh7tBcKe173L3rIYdE4921wbhPfd@bee.rmq.cloudamqp.com/xnennbql'))
    channel = connection.channel()

    channel.queue_declare(queue=cfg['rabbit']['queue'])
    channel.basic_consume(callback,
                        queue=cfg['rabbit']['queue'],
                        no_ack=True)

    print 'Started listening to the queue'
    channel.start_consuming()

if __name__ == '__main__':
    subscribe()