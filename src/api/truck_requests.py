import requests
from lib.config import cfg

def authenticate_incoming(app_id, token):
    pass

def router_login():
    r = requests.post(cfg['requests']['router_base_url'] + '/login', 
                        json={'appId': cfg['requests']['truck_app_id'], 'token': cfg['requests']['token']})

    if r.status_code != 201:
        raise Exception('Login failed with status code %s!' % r.status_code)
    else:
        res = r.json()
        return res['sessionId']


def get_receiver_info(order_id):
    pass

def warehouse_query():
    pass

def update_order_status(order_id):
    pass