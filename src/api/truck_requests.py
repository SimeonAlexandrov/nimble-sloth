import requests
from lib.config import cfg


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

def authenticate_incoming(app_id, token, session_id):
    url = cfg['requests']['router_base_url'] + '/apps/%s' % app_id
    print url
    r = requests.get(url, headers={'X-Auth-Token': session_id})
    
    if r.status_code != 200:
        raise InvalidUsage('Get app profile failed with status code %s!' % r.status_code, r.status_code)
    else:
        res = r.json()
        if res['appId'] != app_id or res['token'] != token:
            raise InvalidUsage('Authenticaton failed', 401)
        else:
            return

def router_login():
    r = requests.post(cfg['requests']['router_base_url'] + '/login', 
                        json={'appId': cfg['requests']['truck_app_id'], 'token': cfg['requests']['token']})

    if r.status_code != 201:
        raise InvalidUsage('Login failed with status code %s!' % r.status_code, status_code)
    else:
        res = r.json()
        return res['sessionId']


def get_receiver_info(order_id):
    pass

def warehouse_query():
    pass

def update_order_status(order_id):
    pass