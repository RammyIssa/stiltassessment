import json
import asyncio
import random
import os

from kitchen.entrypoints.cli import Cli
from kitchen.domain.models import OrderDict
from helpers.enum import StrategyEnum

class Simulator():

    # Simulator runs the CLI
    def __init__(self, strategy: int):
        self.cli = Cli(strategy)
        self.strategy: int = strategy
        self.fifo_pickup_request_count: int = 0

    # Retrieve path of orders to load
    def load_orders_file_path(self, filename: str) -> str:
        curr_path = os.path.dirname(__file__)
        return os.path.join(curr_path, filename)

    # Cylcle through orders and create task to place order and dispatch courier
    async def take_orders(self, filename: str) -> None:
        print(filename)
        f = open(filename)
        orders = json.load(f)
        order_counter: int = 0

        for order in orders:
            order_counter += 1
            order_ob: OrderDict = order
            self.cli.loop.create_task(self.order_food_and_dispatch_courier(order_ob))
            #
            if order_counter % 2 == 0:
                await asyncio.sleep(1)
        
        # wait for all tasks to complete
        while(len(asyncio.all_tasks()) > 1):
            await asyncio.sleep(1)

    # Create CLI task to Dispatch Courier, sleep until courier arrives
    #                               then place him in the waiting queue.
    async def dispatch_courier(self, order: OrderDict) -> None:
        self.cli.loop.create_task(self.cli.dispatch_courier(order))
        await asyncio.sleep(random.randint(3,15))
        self.cli.loop.create_task(self.cli.courier_ready_for_pickup(order))

    # Create CLI task to place Order, sleep until order is ready
    #                               then place order in the waiting queue.
    async def place_order(self, order: OrderDict) -> None:
        self.cli.loop.create_task(self.cli.place_order(order))

        try:
            await asyncio.sleep(order["prepTime"])
        except KeyError:
            return            

        self.cli.loop.create_task(self.cli.order_ready_for_pickup(order))

    # Create CLI task to place order, dispatch courier, and deliver.
    async def order_food_and_dispatch_courier(self, order: OrderDict) -> None:
        if await self.cli.check_fields(order):
            self.cli.loop.create_task(self.place_order(order))
            self.cli.loop.create_task(self.dispatch_courier(order))
            self.cli.loop.create_task(self.pickup_order(order))

    # If order and courier are ready, deliver. Create CLI task to pickup order. 
    async def pickup_order(self, order: OrderDict) -> None:
        try:
            order_is_ready = await self.cli.orderqueue.order_ready(order["id"])
            courier_has_arrived = await self.cli.courierqueue.courier_arrived(order["id"])
        except KeyError:
            return
        
        # Deliver If ready. 
        #   If order and courier are not ready, create tsak to check back later.
        if order_is_ready and courier_has_arrived and self.fifo_pickup_request_count < 1:
            if self.strategy == StrategyEnum.FIFO.value:
                self.fifo_pickup_request_count +=1
            await self.cli.loop.create_task(self.cli.pickup_order(order))
            self.fifo_pickup_request_count -=1
        else:
            self.cli.loop.create_task(self.pickup_order(order))

    # Print stats if Sim is complete
    def finish_sim(self) -> None:
        self.cli.finish_cli()

    # Starting sim, gather orders and begin taking orders, 
    #                               finish sim and print order.
    def start_sim(self) -> None:
        filename = self.load_orders_file_path("dispatch_orders.json")
        self.cli.loop.run_until_complete(self.take_orders(filename))
        self.finish_sim()

        
if __name__ == "__main__":
    strategy: int = 0
    
    # User input, gather strategy to use on waiting queues and Run system.
    while True:
        try:
            print("Please Enter 1 to run the system with FIFO, Enter 2 for Matched.")
            strategy = int(input("Enter Any other number to exit: "))
            if (strategy not in [StrategyEnum.FIFO.value, StrategyEnum.Matched.value]):
                exit()
            sim = Simulator(strategy)
            sim.start_sim()
        except ValueError:
            strategy = 0
            


