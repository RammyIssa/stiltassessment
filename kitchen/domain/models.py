import time
from typing import TypedDict

import os, sys; sys.path.append(os.path.dirname(os.path.realpath(__file__)))

class OrderDict(TypedDict):
    orderid: str
    name: str
    prepTime: int


class Order():
    def __init__(self, order: OrderDict):
        self.orderid: str = order['id']
        self.name: str = order['name']
        self.preptime: int = order['prepTime']


class OrderData():
    def __init__(self, order: Order):
        self.timeorderplaced: float = time.time()
        self.timeorderprepped: float = 0.000
        self.timeorderpickedup: float = 0.000
        self.order: Order = order

    async def update_time_order_prepped(self):
        self.timeorderprepped: float = time.time()


class Courier():
    def __init__(self, order: OrderDict):
        self.orderid: str = order['id']


class CourierData():
    def __init__(self, courier: Courier):
        self.timecourierdispatched: float = time.time()
        self.timecourierarrived: float = 0.0
        self.timecourierpickedup: float = 0.0
        self.courier: Courier = courier

    async def update_time_courier_arrived(self):
        self.timecourierarrived: float = time.time()