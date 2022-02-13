import json
import asyncio
import random
import os

from kitchen.entrypoints.cli import Cli
from kitchen.domain.models import OrderDict
from helpers.enum import StrategyEnum

class Simulator():

    def __init__(self, strategy: int):
        self.cli = Cli(strategy)
        self.strategy: int = strategy
        self.fifo_pickup_request_count: int = 0

    def load_orders_file_path(self, filename: str) -> str:
        curr_path = os.path.dirname(__file__)
        return os.path.join(curr_path, filename)

    async def take_orders(self, filename: str) -> None:
        print(filename)
        f = open(filename)
        orders = json.load(f)
        order_counter = 0

        for order in orders:
            order_counter += 1
            order_ob: OrderDict = order
            self.cli.loop.create_task(self.order_food_and_dispatch_courier(order_ob))
            if order_counter % 2 == 0:
                await asyncio.sleep(1)
        
        while(len(asyncio.all_tasks()) > 1):
            await asyncio.sleep(1)

    async def dispatch_courier(self, order: OrderDict) -> None:
        #slepe then add dispatcher to queue
        self.cli.loop.create_task(self.cli.dispatch_courier(order))
        await asyncio.sleep(random.randint(3,15))
        self.cli.loop.create_task(self.cli.courier_ready_for_pickup(order))

    async def place_order(self, order: OrderDict) -> None:
        #sleep then add order to queue
        self.cli.loop.create_task(self.cli.place_order(order))

        try:
            await asyncio.sleep(order["prepTime"])
        except KeyError:
            return            

        self.cli.loop.create_task(self.cli.order_ready_for_pickup(order))


    async def order_food_and_dispatch_courier(self, order: OrderDict) -> None:
        if await self.cli.check_fields(order):
            self.cli.loop.create_task(self.place_order(order))
            self.cli.loop.create_task(self.dispatch_courier(order))
            self.cli.loop.create_task(self.pickup_order(order))

    async def pickup_order(self, order: OrderDict) -> None:
        try:
            order_is_ready = await self.cli.orderqueue.order_ready(order["id"])
            courier_has_arrived = await self.cli.courierqueue.courier_arrived(order["id"])
        except KeyError:
            return
        
        if order_is_ready and courier_has_arrived and self.fifo_pickup_request_count < 1:
            if self.strategy == StrategyEnum.FIFO.value:
                self.fifo_pickup_request_count +=1
            await self.cli.loop.create_task(self.cli.pickup_order(order))

            self.fifo_pickup_request_count -=1
        else:
            self.cli.loop.create_task(self.pickup_order(order))

    def finish_sim(self) -> None:
        self.cli.finish_cli()

    def start_sim(self) -> None:
        filename = self.load_orders_file_path("dispatch_orders.json")
        self.cli.loop.run_until_complete(self.take_orders(filename))
        self.finish_sim()
        
        
if __name__ == "__main__":
    strategy: int = 0

    while strategy not in [StrategyEnum.FIFO.value, StrategyEnum.Matched.value]:
        try:
            strategy = int(input("Please enter 1 for FIFO and 2 for Matched: "))
        except ValueError:
            strategy = 0
            
    sim = Simulator(strategy)
    sim.start_sim()

