import time
from multiprocessing import Process

from api.app import app
from qsubscriber.subscriber import subscribe

def queue_listener():
    while True:
        print 'Demo listening to queue'
        time.sleep(2)

def main():
    # Setup concurrent execution of web api and message polling
    p = Process(target=subscribe)
    p.daemon = True
    p.start()
    # p.join()
    app.run(debug=True)
    
if __name__ == '__main__':
    main()