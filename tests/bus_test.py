import pytest
import asyncio

from kitchen.service.bus import EventBus

bus = EventBus()
var_to_test_emit = 0
event_name = "change_global_var"


# Used for testing Bus: adding listener 
@pytest.mark.asyncio
async def change_global_var(param: int) -> None:
    global var_to_test_emit 
    var_to_test_emit = param

# Esnure bus adds listener.
def test_add_listener():
    bus.add_listener(event_name, change_global_var)
    assert bus.listeners[event_name] == {change_global_var}

# Ensure bus removes listener.
def test_remove_listener():
    bus.add_listener(event_name, change_global_var)
    bus.remove_listener(event_name, change_global_var)
    with pytest.raises(Exception) as KeyError:
        bus.listeners[event_name] 

# Ensure events that are emitted to the bus are executed.
@pytest.mark.asyncio
async def test_emit():
    param_passed_to_test_emit = 10
    asyncio.new_event_loop()
    bus.add_listener(event_name, change_global_var)
    bus.emit(event_name, param_passed_to_test_emit)
    await asyncio.sleep(1)
    assert var_to_test_emit == param_passed_to_test_emit

