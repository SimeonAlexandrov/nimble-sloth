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
    facade_request = requests.get(cfg['requests']['facade_base_url'] + '/orders/' + cfg['requests']['demo_user_id'] + '/' + order_id, 
                       headers={'X-Auth-Token': cfg['requests']['token']})
    
    print 'Facade request info receiver {}'.format(facade_request.status_code)

def warehouse_put(order, session_id):
    r = requests.get(cfg['requests']['router_base_url'] + '/apps/' + cfg['requests']['warehouse_app_id'], 
                       headers={'X-Auth-Token': session_id})
    profile_result = r.json()
    warehouse_url = profile_result['url']
    print 'Warehouse url obtained %s' % warehouse_url
    print 'Put order with id: {}'.format(order['orderId'])
    put_request = requests.post(warehouse_url + '/orders', json={'id': order['orderId']}, headers={'X-Auth-Token': cfg['requests']['token']})
    print 'Put request %s' % put_request.status_code
    print 'Order {} put to warehouse'.format(order['orderId'])

def warehouse_delete(order_id, session_id):
    r = requests.get(cfg['requests']['router_base_url'] + '/apps/' + cfg['requests']['warehouse_app_id'], 
                       headers={'X-Auth-Token': session_id})
    profile_result = r.json()
    warehouse_url = profile_result['url']
    print 'Warehouse url obtained %s' % warehouse_url

    put_request = requests.delete(warehouse_url + '/orders' + order_id, headers={'X-Auth-Token': cfg['requests']['token']})
    print 'Delete request %s' % put_request.status_code
    print 'Order {} deleted from warehouse'.format(order_id)
    

def update_order_status(status, order_id):
    facade_request = requests.patch(cfg['requests']['facade_base_url'] + '/orders/' + cfg['requests']['demo_user_id'] + '/' + order_id + '.json', 
                       headers={'X-Auth-Token': cfg['requests']['token']},
                       json={'status': status})
    print 'Facade update status {}'.format(facade_request.status_code)
    pass