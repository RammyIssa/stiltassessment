import time
from typing import TypedDict

import os, sys; sys.path.append(os.path.dirname(os.path.realpath(__file__)))

class OrderDict(TypedDict):
    orderid: str
    name: str
    prepTime: int


class Order():
    # Order contains 3 fields
    def __init__(self, order: OrderDict):
        try:
            self.orderid: str = order['id']
            self.name: str = order['name']
            self.preptime: int = order['prepTime']
        except KeyError:
            return


class OrderData():
    # Order data contains order and time orer was 
    #   placed/prepped/pickedup, used to inform outisde world.
    def __init__(self, order: Order):
        self.timeorderplaced: float = time.time()
        self.timeorderprepped: float = 0.000
        self.timeorderpickedup: float = 0.000
        self.order: Order = order

    # Update time order was prepped, used to calculate wait time
    async def update_time_order_prepped(self):
        self.timeorderprepped: float = time.time()


class Courier():
    def __init__(self, order: OrderDict):
        try:
            self.orderid: str = order['id']
        except KeyError:
            return


class CourierData():
    # Courier data contains courier and time courier 
    #   dispatched/arrived/pickedup, used to inform outisde world.
    def __init__(self, courier: Courier):
        self.timecourierdispatched: float = time.time()
        self.timecourierarrived: float = 0.0
        self.timecourierpickedup: float = 0.0
        self.courier: Courier = courier

    # Update time courier arrived, used to calculate wait time.
    async def update_time_courier_arrived(self):
        self.timecourierarrived: float = time.time()