import pika

from lib.config import cfg

def callback(ch, method, properties, body):
        print("Received %r" % body)


def subscribe():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=cfg['rabbit']['host']))
    channel = connection.channel()

    channel.queue_declare(queue=cfg['rabbit']['queue'])
    channel.basic_consume(callback,
                        queue=cfg['rabbit']['queue'],
                        no_ack=True)

    print 'Started listening'
    channel.start_consuming()

if __name__ == '__main__':
    subscribe()