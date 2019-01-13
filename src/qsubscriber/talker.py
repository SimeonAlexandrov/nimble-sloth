import pika
import random
import uuid
import json

def talk():
    
    dummy_order = [
        {
            "orderId": 'order' + str(uuid.uuid4()),
            "pickUp": {
                "latitude": "12.433",
                "longitude": "33.325325"
            },
            "destination": {
                "latitude": "12.43264645",
                "longitude": "33.325324264745"
            }
        },
        {
            "orderId": 'order' + str(uuid.uuid4()),
            "pickUp": {
                "latitude": "12.433",
                "longitude": "33.325325"
            },
            "destination": {
                "latitude": "12.43264645",
                "longitude": "33.325324264745"
            }
        }
    ]
        
    connection = pika.BlockingConnection(pika.URLParameters('amqp://xnennbql:uu7tKh7tBcKe173L3rIYdE4921wbhPfd@bee.rmq.cloudamqp.com/xnennbql'))
    channel = connection.channel()
    channel.queue_declare(queue='nimble-sloth-queue', durable=True)

    message_body = json.dumps(dummy_order)

    channel.basic_publish(exchange='',
                            routing_key='nimble-sloth-queue',
                            body=message_body)

    print 'Sent %s orders' % len(dummy_order)
    connection.close()

if __name__ == '__main__':
    talk()