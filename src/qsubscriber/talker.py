import pika
import random
import uuid
import json

def talk():
    
    dummy_order = {
        'order_id': str(uuid.uuid4()),
        'dest_lng': random.randint(0,100),
        'dest_lat': random.randint(0,100)
    }
        
    connection = pika.BlockingConnection(pika.URLParameters(cfg['rabbit']['url']))
    channel = connection.channel()
    channel.queue_declare(queue='tasks')

    message_body = json.dumps(dummy_order)

    channel.basic_publish(exchange='',
                            routing_key='tasks',
                            body=message_body)

    print 'Sent order with id %s' % dummy_order['order_id']
    connection.close()

if __name__ == '__main__':
    talk()