from kitchen.domain.queue import CourierQueue, OrderQueue
from kitchen.adapters.stats_printer import ConsolePrinter 
from kitchen.domain.models import Courier, CourierData, Order, OrderData
from kitchen.domain.models import OrderDict

class Handlers():
    consoleprinter = ConsolePrinter()
    courierqueue: CourierQueue
    orderqueue: OrderQueue 

    def __init__(self, courierqueue: CourierQueue, orderqueue: OrderQueue):
        Handlers.courierqueue = courierqueue
        Handlers.orderqueue = orderqueue

    async def place_order(order: OrderDict) -> None:
        await Handlers.consoleprinter.print_order_placed(order)

    async def order_ready_for_pickup(order: OrderDict) -> None:
        new_order = OrderData(Order(order))
        await Handlers.orderqueue.add_order(new_order)
        await Handlers.consoleprinter.print_order_prepped(order)

    async def dispatch_courier(order: OrderDict) -> None:
        await Handlers.consoleprinter.print_courier_dispatched(order)

    async def courier_ready_for_pickup(order: OrderDict) -> None:
        new_courier = CourierData(Courier(order))
        await Handlers.courierqueue.add_courier(new_courier)
        await Handlers.consoleprinter.print_courier_arrived(order)

    async def pickup_order(order: OrderDict)-> None:
        orderid = order['id']    
        order_from_queue = await Handlers.orderqueue.remove_order(orderid)
        courier_from_queue = await Handlers.courierqueue.remove_courier(orderid)
        await Handlers.consoleprinter.print_order_stat(
                                    order_from_queue, 
                                        courier_from_queue)
