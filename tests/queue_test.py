import pytest
import time

from kitchen.domain.queue import OrderQueue, CourierQueue
from kitchen.domain.models import CourierData, OrderData, OrderDict, Order, Courier
from helpers.enum import StrategyEnum

temp_order: OrderDict = {
        "id": "5bd1e697-10b2-48cf-83c4-033eea97bfb2", 
        "name": "Pressed Juice", 
        "prepTime": 1
    }

order = Order(temp_order)
courier = Courier(temp_order)
temp_order_queue_FIFO = OrderQueue(StrategyEnum.FIFO.value)
temp_order_queue_matched = OrderQueue(StrategyEnum.Matched.value)
temp_courier_queue_FIFO = CourierQueue(StrategyEnum.FIFO.value)
temp_courier_queue_matched = CourierQueue(StrategyEnum.Matched.value)

temp_courierdata = CourierData(order)
temp_orderdata = OrderData(courier)

@pytest.mark.asyncio
async def test_is_empty() -> None:
    assert await temp_order_queue_FIFO.is_empty() == True
    assert await temp_order_queue_matched.is_empty() == True
    assert await temp_courier_queue_FIFO.is_empty() == True
    assert await temp_courier_queue_matched.is_empty() == True

@pytest.mark.asyncio
async def test_add_order() -> None:
    await temp_order_queue_FIFO.add_order(temp_orderdata)
    await temp_order_queue_matched.add_order(temp_orderdata)
    assert await temp_order_queue_FIFO.order_ready(temp_orderdata.order.orderid) == True
    assert await temp_order_queue_matched.order_ready(temp_orderdata.order.orderid) == True

@pytest.mark.asyncio
async def test_add_courier() -> None:
    await temp_courier_queue_FIFO.add_courier(temp_courierdata)
    await temp_courier_queue_matched.add_courier(temp_courierdata)
    assert await temp_courier_queue_FIFO.courier_arrived(temp_courierdata.courier.orderid) == True
    assert await temp_courier_queue_matched.courier_arrived(temp_courierdata.courier.orderid) == True

@pytest.mark.asyncio
async def test_courier_arrived() -> None:
    assert await temp_courier_queue_FIFO.courier_arrived(temp_courierdata.courier.orderid) == True
    assert await temp_courier_queue_matched.courier_arrived(temp_courierdata.courier.orderid) == True

@pytest.mark.asyncio
async def test_order_ready() -> None:
    assert await temp_order_queue_FIFO.order_ready(temp_orderdata.order.orderid) == True
    assert await temp_order_queue_matched.order_ready(temp_orderdata.order.orderid) == True


@pytest.mark.asyncio
async def test_remove_order() -> None:
    await temp_order_queue_FIFO.add_order(temp_orderdata)
    await temp_order_queue_matched.add_order(temp_orderdata)
    assert await temp_order_queue_FIFO.remove_order(temp_orderdata.order.orderid) == temp_orderdata
    assert await temp_order_queue_matched.remove_order(temp_orderdata.order.orderid) == temp_orderdata

@pytest.mark.asyncio
async def test_remove_courier() -> None:
    await temp_courier_queue_FIFO.add_courier(temp_courierdata)
    await temp_courier_queue_matched.add_courier(temp_courierdata)
    assert await temp_courier_queue_FIFO.remove_courier(temp_courierdata.courier.orderid) == temp_courierdata
    assert await temp_courier_queue_matched.remove_courier(temp_courierdata.courier.orderid) == temp_courierdata

@pytest.mark.asyncio
async def test_calc_order_wait_time() -> None:
    await temp_order_queue_FIFO.add_order(temp_orderdata)
    await temp_order_queue_matched.add_order(temp_orderdata)
    time.sleep(0.1)
    await temp_order_queue_FIFO.remove_order(temp_orderdata.order.orderid)
    await temp_order_queue_matched.remove_order(temp_orderdata.order.orderid)
    assert temp_order_queue_FIFO.calc_order_wait_time() > 0.0
    assert temp_order_queue_matched.calc_order_wait_time() > 0.0

@pytest.mark.asyncio
async def test_calc_courier_wait_time() -> None:
    await temp_courier_queue_FIFO.add_courier(temp_courierdata)
    await temp_courier_queue_matched.add_courier(temp_courierdata)
    time.sleep(0.1)
    await temp_courier_queue_FIFO.remove_courier(temp_courierdata.courier.orderid)
    await temp_courier_queue_matched.remove_courier(temp_courierdata.courier.orderid)
    assert temp_courier_queue_FIFO.calc_courier_wait_time() > 0.0
    assert temp_courier_queue_matched.calc_courier_wait_time() > 0.0
