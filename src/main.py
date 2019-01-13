import time
from multiprocessing import Process
from multiprocessing import Manager
from mongoengine import connect

from api.app import app
from api.truck_requests import router_login
from lib.config import cfg
from qsubscriber.subscriber import subscribe

def init_truck_data(truck_data_object):
    truck_data_object['truck_id'] = cfg['requests']['truck_app_id']
    truck_data_object['status'] = 'CHILLIN_IN_WAREHOUSE'
    truck_data_object['lat'] = 'WAREHOUSE_LAT'
    truck_data_object['lng'] = 'WAREHOUSE_LNG'
    truck_data_object['capacity'] = 100

def main():
    manager = Manager()
    # Init truck general data 
    truck_data = manager.dict()
    init_truck_data(truck_data)
    
    # Obtain session id from router
    session_id = router_login()

    # Setup concurrent execution of web api and message polling
    p = Process(target=subscribe, args=(session_id, truck_data))
    p.daemon = True
    p.start()

    app.config['session_id'] = session_id
    app.config['truck_data'] = truck_data
    
    app.run(host='0.0.0.0', port=cfg['api']['port'])
    p.join()
    
if __name__ == '__main__':
    main()