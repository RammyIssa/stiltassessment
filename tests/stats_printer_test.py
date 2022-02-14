import pytest

from kitchen.adapters.stats_printer import ConsolePrinter
from kitchen.domain.models import OrderDict

temp_order: OrderDict = {
        "id": "5bd1e697-10b2-48cf-83c4-033eea97bfb2", 
        "name": "Pressed Juice", 
        "prepTime": 1
}
    
temp_console_printer = ConsolePrinter()

# Tests to ensure adapter is working and outside world has 
#                               visibility to system operations.

@pytest.mark.asyncio
async def test_print_order_placed(capsys) -> None:
    await temp_console_printer.print_order_placed(temp_order)
    captured = capsys.readouterr()
    assert temp_order["name"] in captured.out
    assert temp_order["id"] in captured.out
    
@pytest.mark.asyncio
async def test_print_order_prepped(capsys) -> None:
    await temp_console_printer.print_order_prepped(temp_order)
    captured = capsys.readouterr()
    assert temp_order["name"] in captured.out
    assert temp_order["id"] in captured.out

@pytest.mark.asyncio
async def test_print_courier_dispatched(capsys) -> None:
    await temp_console_printer.print_courier_dispatched(temp_order)
    captured = capsys.readouterr()
    assert temp_order["id"] in captured.out

@pytest.mark.asyncio
async def test_print_courier_arrived(capsys) -> None:
    await temp_console_printer.print_courier_arrived(temp_order)
    captured = capsys.readouterr()
    assert temp_order["id"] in captured.out