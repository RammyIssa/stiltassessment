import asyncio
import pytest

from kitchen.domain.models import OrderDict
from kitchen.entrypoints.cli import Cli
from helpers.enum import StrategyEnum

temp_prepTime = 1
temp_order: OrderDict = {
        "id": "5bd1e697-10b2-48cf-83c4-033eea97bfb2", 
        "name": "Pressed Juice", 
        "prepTime": temp_prepTime
    }
temp_bad_order: OrderDict = {
        "wrongid": "5bd1e697-10b2-48cf-83c4-033eea97bfb2", 
        "wrongname": "Pressed Juice", 
        "wrongprepTime": temp_prepTime    
}
temp_cli = Cli(StrategyEnum.Matched.value)

# Ensures check_fields() catches good input and bad input, and 
#                               communicates with the outisde world.
@pytest.mark.asyncio
async def test_check_fields(capsys) -> None:
    global temp_order, temp_cli, temp_bad_order

    assert await temp_cli.check_fields(temp_order) == True  
    await temp_cli.check_fields(temp_bad_order)
    await asyncio.sleep(1)
    captured = capsys.readouterr()
    assert "Incorrect fields" in captured.out

# Esnure dispatch_courier() is passed to the bus and 
#               communicates task with the outside world.
@pytest.mark.asyncio
async def test_dispatch_courier(capsys) -> None:
    global temp_order, temp_cli    
    await temp_cli.dispatch_courier(temp_order)
    await asyncio.sleep(1)
    captured = capsys.readouterr()
    assert temp_order["id"] in captured.out

# Ensure place_order() is passed to the bus and 
#               communicates task to outside world.
@pytest.mark.asyncio
async def test_place_order(capsys) -> None:
    global temp_order, temp_cli    
    await temp_cli.place_order(temp_order)
    await asyncio.sleep(1)
    captured = capsys.readouterr()
    assert temp_order["id"] in captured.out

# Ensures order_ready_for_pickup() is passed to the bus and 
#                           communicates task the outside world.
@pytest.mark.asyncio
async def test_order_ready_for_pickup(capsys) -> None:
    global temp_order, temp_cli    
    await temp_cli.order_ready_for_pickup(temp_order)
    await asyncio.sleep(2)
    captured = capsys.readouterr()
    assert temp_order["id"] in captured.out

# Ensures courier_ready_for_pickup() is passed to the bus and 
#                           communicates task to the outside world.
@pytest.mark.asyncio
async def test_courier_ready_for_pickup(capsys) -> None:
    global temp_order, temp_cli    
    await temp_cli.courier_ready_for_pickup(temp_order)
    await asyncio.sleep(1)
    captured = capsys.readouterr()
    assert temp_order["id"] in captured.out

# Ensures pickup_order() is passed to the bus and   
#               communicates task to the outside world.
@pytest.mark.asyncio
async def test_pickup_order(capsys) -> None:
    global temp_order, temp_cli    
    await temp_cli.pickup_order(temp_order)
    await asyncio.sleep(1)
    captured = capsys.readouterr()
    assert temp_order["id"] in captured.out

# Ensures finish_cli() communicates averages to the outisde world.
@pytest.mark.asyncio
async def test_finish_cli(capsys) -> None:
    global temp_order, temp_cli    
    temp_cli.finish_cli()
    captured = capsys.readouterr()
    assert "Average Courier Wait Time" in captured.out
    assert "Average Food Wait Time" in captured.out

