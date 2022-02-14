import pytest

from kitchen.domain.queue import OrderQueue, CourierQueue
from kitchen.domain.models import OrderDict
from kitchen.service.eventhandlers import Handlers
from helpers.enum import StrategyEnum

temp_order: OrderDict = {
        "id": "5bd1e697-10b2-48cf-83c4-033eea97bfb2", 
        "name": "Pressed Juice", 
        "prepTime": 1
    }

temp_order_queue = OrderQueue(StrategyEnum.Matched.value)
temp_courier_queue = CourierQueue(StrategyEnum.Matched.value)

temp_handlers = Handlers(temp_courier_queue, temp_order_queue)

# Ensure place_order() communicates task to the outside world.
@pytest.mark.asyncio
async def test_place_order(capsys) -> None:
    await Handlers.place_order(temp_order)
    captured = capsys.readouterr()
    assert temp_order["id"] in captured.out

# Ensure order_ready_for_pickup() adds order to queue 
#               and communicates task to the outside world.
@pytest.mark.asyncio
async def test_order_ready_for_pickup(capsys) -> None:
    await Handlers.order_ready_for_pickup(temp_order)
    captured = capsys.readouterr()
    assert temp_order["id"] in captured.out
    assert await temp_order_queue.order_ready(temp_order["id"]) == True

# Ensure dispatch_courier() communicates task to the outside world.
@pytest.mark.asyncio
async def test_dispatch_courier(capsys) -> None:
    await Handlers.dispatch_courier(temp_order)
    captured = capsys.readouterr()
    assert temp_order["id"] in captured.out

# Ensure courier_ready_for_pickup adds courier to queue 
#                   and communicates to the outisde world.
@pytest.mark.asyncio
async def test_courier_ready_for_pickup(capsys) -> None:
    await Handlers.courier_ready_for_pickup(temp_order)
    captured = capsys.readouterr()
    assert temp_order["id"] in captured.out
    assert await temp_courier_queue.courier_arrived(temp_order["id"]) == True

# Ensure pickup_order() removes order and courier from queue 
#                           and communicates to the outisde world.
@pytest.mark.asyncio
async def test_pickup_order(capsys)-> None:
    await Handlers.pickup_order(temp_order)
    captured = capsys.readouterr()
    assert temp_order["id"] in captured.out
    assert await temp_courier_queue.courier_arrived(temp_order["id"]) == False
    assert await temp_order_queue.order_ready(temp_order["id"]) == False