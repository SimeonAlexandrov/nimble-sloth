import time
from multiprocessing import Process
from mongoengine import connect

from api.app import app
from lib.config import cfg
from qsubscriber.subscriber import subscribe

def main():
    # Setup concurrent execution of web api and message polling
    p = Process(target=subscribe)
    p.daemon = True
    p.start()
    app.run(host='0.0.0.0', port=cfg['api']['port'])
    p.join()
    
if __name__ == '__main__':
    main()