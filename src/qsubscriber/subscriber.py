import pika

def callback(ch, method, properties, body):
        print("Received %r" % body)


def subscribe():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='tasks')
    channel.basic_consume(callback,
                        queue='tasks',
                        no_ack=True)

    print 'Started listening'
    channel.start_consuming()

if __name__ == '__main__':
    subscribe()