from kitchen.domain.models import CourierData, OrderData, OrderDict
from datetime import datetime

DATE_FORMAT = '%Y-%m-%d %H:%M:%S.%f'

class ConsolePrinter():
    def __init__(self):
        pass

    # Helper function to generate current time, 
    #                   used for realtime tracking.
    async def return_formatted_curr_time(self):
        return (datetime.utcnow().strftime(DATE_FORMAT)[:-3])

    # Inform outside world of order/courier wait time for an oder.
    async def print_order_stat(self, orderdata: OrderData, 
                                            courierdata: CourierData) -> None:
        curr_time = await self.return_formatted_curr_time()
        orderid = orderdata.order.orderid
        foodwaittime = orderdata.timeorderpickedup - orderdata.timeorderprepped
        courierwaittime = courierdata.timecourierpickedup - courierdata.timecourierarrived
        print("\n%s - ORDER PICKED UP: \t%s\nFood Wait Time: %i milliseconds\nCourier Wait Time: %i milliseconds\n" % 
                    (
                        curr_time , orderid, (foodwaittime * 1000), (courierwaittime * 1000)
                    ) 
        )

    # Inform outside world of average courier/order wait times.
    def print_average_order_stat(self, courieraverage: float, orderaverage: float) -> None:
        print("Average Courier Wait Time: %i milliseconds\nAverage Food Wait Time: %i milliseconds\n" % 
                                                (
                                                    (courieraverage * 1000), (orderaverage * 1000)
                                                )
        )

    # Inform outisde world an order was placed.
    async def print_order_placed(self, order: OrderDict) -> None:
        curr_time = await self.return_formatted_curr_time()
        try:
            print("%s - Order Placed:  \t%s - %s" % 
                (
                    curr_time, order["id"], order["name"]
                )
            )
        except KeyError:
            return

    # Inform outside world an order was finished cooking.
    async def print_order_prepped(self, order: OrderDict) -> None:
        curr_time = await self.return_formatted_curr_time()
        try:
            print("%s - Order Prepped:  \t%s - %s"% 
                (
                    curr_time, order["id"], order["name"]
                )
            )
        except KeyError:
            return

    # Inform outisde world that a courier has been dispatched.
    async def print_courier_dispatched(self, order: OrderDict) -> None:
        curr_time = await self.return_formatted_curr_time()
        try:
            print("%s - Courier Dispatched: \t%s " % (curr_time,order["id"]))
        except KeyError:
            return

    # Inform outisde world that a courier has arrived for pickup.
    async def print_courier_arrived(self, order: OrderDict) -> None:
        curr_time = await self.return_formatted_curr_time()
        try:
            print("%s - Courier Arrived: \t%s "% (curr_time,order["id"]))
        except KeyError:
            return
            
    # Used to inform outisde world an order was not valid.
    async def print_exception(e: Exception) -> None:
        print(e)


