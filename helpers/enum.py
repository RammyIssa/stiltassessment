from enum import Enum, IntEnum

class StrategyEnum(IntEnum):
    FIFO = 1
    Matched = 2

class EventHandlersEnum(Enum):
    PlaceOrder = "place_order"
    DispatchCourier = "dispatch_courier"
    PickupOrder = "pickup_order"
    CourierReadyForPickup = "courier_ready_for_pickup"
    OrderReadyForPickup = "order_ready_for_pickup"
