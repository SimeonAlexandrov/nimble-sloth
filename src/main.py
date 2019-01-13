import time
from multiprocessing import Process
from mongoengine import connect

from api.app import app
from api.truck_requests import router_login
from lib.config import cfg
from qsubscriber.subscriber import subscribe

def main():
    # Obtain session id from router
    session_id = router_login()

    # Setup concurrent execution of web api and message polling
    p = Process(target=subscribe, args=(session_id,))
    p.daemon = True
    p.start()
    app.config['session_id'] = session_id
    app.run(host='0.0.0.0', port=cfg['api']['port'])
    p.join()
    
if __name__ == '__main__':
    main()