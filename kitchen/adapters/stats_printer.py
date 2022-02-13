from kitchen.domain.models import CourierData, OrderData, OrderDict
from datetime import datetime

DATE_FORMAT = '%Y-%m-%d %H:%M:%S.%f'

class ConsolePrinter():
    def __init__(self):
        pass

    async def return_formatted_curr_time(self):
        return (datetime.utcnow().strftime(DATE_FORMAT)[:-3])

    async def print_order_stat(self, orderdata: OrderData, 
                                            courierdata: CourierData) -> None:
        curr_time = await self.return_formatted_curr_time()
        orderid = orderdata.order.orderid
        foodwaittime = orderdata.timeorderpickedup - orderdata.timeorderprepped
        courierwaittime = courierdata.timecourierpickedup - courierdata.timecourierarrived
        print("\n%s - ORDER PICKED UP: \t%s\nFood Wait Time: %i milliseconds\nCourier Wait Time: %i milliseconds\n" % (
                                              curr_time , orderid, (foodwaittime * 1000), (courierwaittime * 1000)
                                            ) 
        )

    def print_average_order_stat(self, courieraverage: float, orderaverage: float) -> None:
        print("Average Courier Wait Time: %i milliseconds\nAverage Food Wait Time: %i milliseconds" % 
                                                ((courieraverage * 1000), orderaverage * 1000)
        )

    async def print_order_placed(self, order: OrderDict) -> None:
        curr_time = await self.return_formatted_curr_time()
        print("%s - Order Placed:  \t%s - %s"% (curr_time, order["id"], order["name"]))

    async def print_order_prepped(self, order: OrderDict) -> None:
        curr_time = await self.return_formatted_curr_time()
        print("%s - Order Prepped:  \t%s - %s"% (curr_time, order["id"], order["name"]))

    async def print_courier_dispatched(self, order: OrderDict) -> None:
        curr_time = await self.return_formatted_curr_time()
        print("%s - Courier Dispatched: \t%s " % (curr_time,order["id"]))

    async def print_courier_arrived(self, order: OrderDict) -> None:
        curr_time = await self.return_formatted_curr_time()
        print("%s - Courier Arrived: \t%s "% (curr_time,order["id"]))

    async def print_exception(self, e: Exception) -> None:
        print(e)


