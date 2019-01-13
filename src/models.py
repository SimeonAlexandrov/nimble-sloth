from mongoengine import *
from lib.config import cfg

class Order(Document):
    order_id = StringField(required=True)
    
    src_lng = FloatField()
    src_lat = FloatField()
    
    dest_lng = FloatField()
    dest_lat = FloatField()

    status = StringField()
    recipient_name = StringField()
    recipient_phone = StringField()

class Truck(Document):
    truck_id = StringField(required=True)
    truck_lng = FloatField()
    truck_lat = FloatField()
    status = StringField()
    