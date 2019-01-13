from mongoengine import *
from lib.config import cfg

class Order(Document):
    order_id = StringField(required=True)
    
    src_lng = StringField()
    src_lat = StringField()
    
    dest_lng = StringField()
    dest_lat = StringField()

    status = StringField()
    recipient_name = StringField()
    recipient_phone = StringField()