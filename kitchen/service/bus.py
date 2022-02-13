import asyncio

from helpers.enum import EventHandlersEnum
from kitchen.service.eventhandlers import Handlers


class EventBus():
  def __init__(self):
    self.listeners = {}
    self.add_listener(EventHandlersEnum.PlaceOrder.value, Handlers.place_order)
    self.add_listener(EventHandlersEnum.DispatchCourier.value, Handlers.dispatch_courier)
    self.add_listener(EventHandlersEnum.PickupOrder.value, Handlers.pickup_order)
    self.add_listener(EventHandlersEnum.CourierReadyForPickup.value, Handlers.courier_ready_for_pickup)
    self.add_listener(EventHandlersEnum.OrderReadyForPickup.value, Handlers.order_ready_for_pickup)

  def add_listener(self, event_name: str, listener) -> None:
    if not self.listeners.get(event_name, None):
      self.listeners[event_name] = {listener}
    else:
      self.listeners[event_name].add(listener)

  def remove_listener(self, event_name: str, listener) -> None:
    self.listeners[event_name].remove(listener)
    if len(self.listeners[event_name]) == 0:
      del self.listeners[event_name]

  def emit(self, event_name: str, event) -> None:
    listeners = self.listeners.get(event_name, [])
    for listener in listeners:
      asyncio.create_task(listener(event))    

