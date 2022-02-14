import asyncio
from collections import deque

from kitchen.service.bus import EventBus
from kitchen.service.eventhandlers import Handlers
from kitchen.domain.queue import CourierQueue, OrderQueue
from kitchen.domain.models import OrderDict
from kitchen.adapters.stats_printer import ConsolePrinter
from helpers.enum import EventHandlersEnum


class Cli():
    def __init__(self, strategy: int):
        self.loop = asyncio.new_event_loop()
        self.bus = EventBus()
        self.courierqueue = CourierQueue(strategy)
        self.orderqueue = OrderQueue(strategy)
        self.handlers = Handlers(self.courierqueue, self.orderqueue)
        self.fields: deque[str] = ["id", "prepTime", "name"]
        asyncio.set_event_loop(self.loop)

    # Ensure order has appropriate fields.
    async def check_fields(self, order: OrderDict) -> bool:
        if all(field in order for field in self.fields):
            return True
        e = "Incorrect fields for order: " + str(order)
        await ConsolePrinter.print_exception(e)
        return False

    # Add Dispatch courier event to bus.
    async def dispatch_courier(self, order: OrderDict) -> None:
        if await self.check_fields(order):
            self.bus.emit(EventHandlersEnum.DispatchCourier.value, order)

    # Add place order event to bus.
    async def place_order(self, order: OrderDict) -> None:
        if await self.check_fields(order):
            self.bus.emit(EventHandlersEnum.PlaceOrder.value, order)

    # Add order ready event to bus.
    async def order_ready_for_pickup(self, order: OrderDict) -> None:
        if await self.check_fields(order):
            self.bus.emit(EventHandlersEnum.OrderReadyForPickup.value, order)

    # Add courier ready event to bus.
    async def courier_ready_for_pickup(self, order: OrderDict) -> None:
        if await self.check_fields(order):
            self.bus.emit(EventHandlersEnum.CourierReadyForPickup.value, order)

    # Add pickup order event to bus.
    async def pickup_order(self, order: OrderDict) -> None:
        if await self.check_fields(order):
            self.bus.emit(EventHandlersEnum.PickupOrder.value, order)

    # Let outisde world know of average food/courier wait times.
    def finish_cli(self) -> None:
        Handlers.consoleprinter.print_average_order_stat(
            Handlers.courierqueue.calc_courier_wait_time(), 
                Handlers.orderqueue.calc_order_wait_time()
        )
        