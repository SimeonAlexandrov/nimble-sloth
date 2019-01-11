import pika

def talk():
        
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='tasks')

    channel.basic_publish(exchange='',
                            routing_key='tasks',
                            body='HelloWorld!')

    print 'sent hw'
    connection.close()

if __name__ == '__main__':
    talk()