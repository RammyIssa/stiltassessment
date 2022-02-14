import pytest

from kitchen.domain.models import Order, OrderData, Courier, CourierData

order = {
    "id": "5bd1e697-10b2-48cf-83c4-033eea97bfb2", 
    "name": "Pressed Juice", 
    "prepTime": 1
}

# Ensure update_time_order_prepped() updates time of order object
@pytest.mark.asyncio
async def test_update_time_order_prepped() -> None:
    temp_order = Order(order)
    temp_order_data = OrderData(temp_order)
    await temp_order_data.update_time_order_prepped()
    assert temp_order_data.timeorderprepped > 0.0

# Ensure update_time_courier_arrived() updates time of courier object
@pytest.mark.asyncio
async def test_update_time_courier_arrived() -> None:
    temp_order = Courier(order)
    temp_order_data = CourierData(temp_order)
    await temp_order_data.update_time_courier_arrived()
    assert temp_order_data.timecourierarrived > 0.0
    
