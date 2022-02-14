from collections import deque
import time
from typing import TypedDict

from kitchen.adapters.stats_printer import ConsolePrinter
from .models import CourierData, OrderData
from helpers.enum import StrategyEnum

class OrderMatchedQueue(TypedDict):
    orderid: OrderData

class CourierMatchedQueue(TypedDict):
    orderid: CourierData

class OrderQueue():
    # FIFO queue and dict for matched 
    def __init__(self, strategy: int):
        self.matchedqueue: OrderMatchedQueue = OrderMatchedQueue()
        self.fifoqueue: deque[OrderData] = []
        self.strategy: int = strategy
        self.totalfoodwaittime: float = 0.0
        self.ordercount: int = 0

    # Check if queue is empty. This is used to deliver order if 
    #                                               strategy is FIFO.
    async def is_empty(self) -> bool:
        if self.strategy == StrategyEnum.FIFO.value:
            return not len(self.fifoqueue)
        else:
            return not self.matchedqueue

    # Check if order has been prepped and ready for pickup.
    async def order_ready(self, orderid: str) -> bool:
        if self.strategy == StrategyEnum.FIFO.value:
            return not await self.is_empty()
        else: 
            if orderid in self.matchedqueue.keys():
                return True
            else:
                return False

    # Add order to queue and update time order was prepped.
    async def add_order(self, new_order: OrderData) -> None:
        new_order.timeorderprepped = time.time()
        self.ordercount += 1
        if self.strategy == StrategyEnum.FIFO.value:
            self.fifoqueue.append(new_order)
        else:
            self.matchedqueue[new_order.order.orderid] = new_order

    # Remove order from queue and update time order was picked up
    #                           to inform outside world of wait time.
    async def remove_order(self, orderid: str) -> OrderData:
        try:
            if self.strategy == StrategyEnum.FIFO.value:
                removed_order = self.fifoqueue.pop(0)
            else:
                removed_order = self.matchedqueue.pop(orderid)
                    
            removed_order.timeorderpickedup = time.time()
            self.totalfoodwaittime += (removed_order.timeorderpickedup - removed_order.timeorderprepped)
            return removed_order
        except Exception as e:
            await ConsolePrinter.print_exception(e)

    # Calc average food wait time to inform outside world.
    def calc_order_wait_time(self) -> float:
        try:
            return self.totalfoodwaittime / self.ordercount
        except ZeroDivisionError:
            return 0

class CourierQueue():
    # FIFO queue and dict for matched 
    def __init__(self, strategy: int):
        self.matchedqueue: CourierMatchedQueue = CourierMatchedQueue()
        self.fifoqueue: deque[CourierData] = []
        self.strategy: int = strategy
        self.totalcourierwaittime: float = 0.0
        self.couriercount: int = 0

    # Check if queue is empty. This is used to deliver order if 
    #                                               strategy is FIFO.
    async def is_empty(self) -> bool:
        if self.strategy == StrategyEnum.FIFO.value:
            return bool(not len(self.fifoqueue))
        else:
            return bool(not self.matchedqueue)

    # Check if order has been prepped and ready for pickup.
    async def courier_arrived(self, orderid: str) -> bool:
        if self.strategy == StrategyEnum.FIFO.value:
            return not await self.is_empty()
        else: 
            if orderid in self.matchedqueue.keys():
                return True
            else:
                return False

    # Add courier to queue since he has arrived.
    async def add_courier(self, new_courier: CourierData) -> None:
        new_courier.timecourierarrived = time.time()
        self.couriercount += 1
        if self.strategy == StrategyEnum.FIFO.value:
            self.fifoqueue.append(new_courier)
        else:
            self.matchedqueue[new_courier.courier.orderid] = new_courier

    # Remove courier from queue and update time courier picked up order
    #                                   to inform outside world of wait time.
    async def remove_courier(self, orderid: str) -> CourierData:
        try:
            if self.strategy == StrategyEnum.FIFO.value:
                removed_courier = self.fifoqueue.pop(0)
            else:
                removed_courier = self.matchedqueue.pop(orderid)

            removed_courier.timecourierpickedup = time.time()
            self.totalcourierwaittime += (removed_courier.timecourierpickedup - removed_courier.timecourierarrived)
            return removed_courier
        except Exception as e:
            await ConsolePrinter.print_exception(e)

    # Calc average courier wait time to inform outside world.
    def calc_courier_wait_time(self) -> float:
        try:
            return self.totalcourierwaittime / self.couriercount
        except ZeroDivisionError:
            return 0
