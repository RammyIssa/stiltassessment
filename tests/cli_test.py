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
    
temp_cli = Cli(StrategyEnum.Matched.value)

@pytest.mark.asyncio
async def test_dispatch_courier(capsys) -> None:
    global temp_order, temp_cli    
    await temp_cli.dispatch_courier(temp_order)
    await asyncio.sleep(1)
    captured = capsys.readouterr()
    assert temp_order["id"] in captured.out

@pytest.mark.asyncio
async def test_place_order(capsys) -> None:
    global temp_order, temp_cli    
    await temp_cli.place_order(temp_order)
    await asyncio.sleep(1)
    captured = capsys.readouterr()
    assert temp_order["id"] in captured.out

@pytest.mark.asyncio
async def test_order_ready_for_pickup(capsys) -> None:
    global temp_order, temp_cli    
    await temp_cli.order_ready_for_pickup(temp_order)
    await asyncio.sleep(1)
    captured = capsys.readouterr()
    assert temp_order["id"] in captured.out

@pytest.mark.asyncio
async def test_courier_ready_for_pickup(capsys) -> None:
    global temp_order, temp_cli    
    await temp_cli.courier_ready_for_pickup(temp_order)
    await asyncio.sleep(1)
    captured = capsys.readouterr()
    assert temp_order["id"] in captured.out

@pytest.mark.asyncio
async def test_pickup_order(capsys) -> None:
    global temp_order, temp_cli    
    await temp_cli.pickup_order(temp_order)
    await asyncio.sleep(1)
    captured = capsys.readouterr()
    assert temp_order["id"] in captured.out

async def test_finish_cli(capsys) -> None:
    global temp_order, temp_cli    
    temp_cli.finish_cli()
    captured = capsys.readouterr()
    assert "Average Courier Wait Time" in captured.out
    assert "Average Food Wait Time" in captured.out

