# stilt_assessment
This project is a real-time system that fulfills delivery orders for a kitchen.
The Simulation receives 2 delivery orders per second from the dispatch_orders.json file. Each order
takes some time (defined as `prepTime` in order JSON) to be prepared. Once an order
is prepared, it is waiting and ready for courier pickup.
Upon receiving an order, the system immediately dispatches a courier to pick it up.
Couriers arrive randomly following a uniform distribution, 3-15 seconds after they've
been dispatched. Couriers have to wait at the kitchen if the order they are picking up is
not ready.
Once an order is picked up by a courier it is instantaneously delivered. The system contains 2
courier dispatch strategies:
● Matched: a courier is dispatched for a specific order and may only pick up that
order
● First-in-first-out: a courier picks up the next available order upon arrival.
If there are multiple orders available, the courier picks up an arbitrary order.
If there are no available orders, couriers wait for the next available one. When 
there are multiple couriers waiting, the next available order is assigned to the 
earliest arrived courier. Statistics are printed each time an order is picked up. After the system
has finished processing all orders, an average of each of the statistics are printed, which includes:

● Average food wait time (milliseconds) between order ready and pickup

● Average courier wait time (milliseconds) between arrival and order pickup

In Designing the system, 3 patterns were :
1. Domain Driven Design 
2. Event Driven Architecture
3. Test Driven Design

Domain Driven Design(DDD): DDD is useful when tackling a complex problem. When a system has many moving parts, its sometimes advantages to serparte the system into each of their categories. The system was separated into 4 components. We have the service, which consists of the event bus and the event handlers(More on this in Event Driven Architecture, below). When an order is made, or an order is ready, or a courier needs to be dispatched, or an order is ready for pickup, we emit this event to the bus, where the handlers for those events are listening. The handlers provide the service and means to which our system operates but other parts of the system don't need to be involved with the services that are provided. We also have the adapter, which provides the system a means to communicate with the outside world, and allows the system to display the System's current actions. Additionally, we have the domain layer, which contains the business logic, this is where couriers are added to the waiting queue, or where orders are added to the waiting queue. This is where checking if an order is prepared or if a courier has arrived is done. And lastly, we have the entry points to the system. This is the API, where we can communicate with the system.

Event Driven Architecture(EDA): This system relies on notifications or events. When an order needs is being placed, send an Event! When an order is ready, send an event! When a courier has arrived for an order, SEND AN EVENT! The system relies on this Architecture which helps decouple different parts of the system. The system only reacts to the events. The system revolves around a courier arriving, or an being prepped, or an order being placed, and so on. The system reacts to these events, and is notified so it can take take the appropriate action.

Test Driven Development(TDD): When developing parts of the system, its important to know what each component should do. Using TDD can help ensure each domain stays on its original course and ensure each componenet functions correctly.

Design Decisions:
The system was created to run asyncrnously. The Kitchen places an order and has to wait for the food to cook (Similiar to waiting fo IO). The time it takes to cook this food shouldn't be spent looking at the food and waiting for it to cook, it should be spent on other tasks like taking other orders, dispatching couriers, checking if a courier's order is ready so he/she can pick it up! Python's Asyncio IO package was used so multiple tasks can run concurrently while other tasks are waiting. The event bus was implemented as a way to notify the system. There are multiple tasks that are running, and if one of those tasks are completed, the system should be notified.

Is valid, runnable code (via CLI or IDE)
● Is production-quality code; API implementations are clean and public APIs are
● documented (as if someone had to maintain your system)
● Has appropriate usage of design patterns, concurrency, and data structures
● Has comprehensive unit testing
● Has a README that explains how to operate the system, how design decisions
are
● made, and how to adjust the configurations under which it can be run.
● Has console output that allows interviewers to understand your system's
operation
● as it runs in real-time. Output events (order received, order prepared, courier
● dispatched, courier arrived, order picked up) as they occur so the operation of
your system can be understood as it runs
