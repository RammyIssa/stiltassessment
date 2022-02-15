# stiltassessment
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

# Install and Run
There are 2 different ways to run the application, pulling the container from docker, or cloning the repo and running it locally.

## Docker install and run (copy and paste steps 1-3 in shell)
1. docker run -it rammyissa/code-challenge:stiltAssessmentContainer bash -c "glow -p README.md && bash"
2. Go through readme by hitting Enter. To exit README, simply press `q` 
3. Now you can run the application, type "python3 simulator.py" and press enter
3. Read directions of prompt and enter 1 for FIFO or 2 for matched and press enter to start program, enter any other number to exit program. 
4. Once program is exited and you want to run tests, type "python3 -m pytest" and press enter

## Gibhub clone and run locally
1. git clone https://github.com/RammyIssa/stiltassessment.git
2. cd into main directory '/stiltassessment'
3. create virtual environment with venv or conda
4. activate virtual environment
5. pip3 install -r requirements.txt
6. run application with 'python3 simulator.py'
7. Read directions of prompt and enter 1 for FIFO or 2 for matched and press enter to start program, enter any other number to exit program. 
8. Once program is exited and you want to run tests, type "python3 -m pytest" and press enter

# Entry Points to the system:
### def place_order(order)
#### Description:
Receives order and Informs outside world that the order was placed..
#### args:
order: {
    id: "ID of order",
    name: "description of order",
    prepTime: "integer value representing the number of seconds to prep the food"
}
#### Returns:
None

### def dispatch_courier(order)
#### Description:
Dispatches courier for an order and Informs outside world that the courier was dispatched.
#### args:
order: {
    id: "ID of order",
    name: "description of order",
    prepTime: "integer value representing the number of seconds to prep the food"
}
#### Returns:
None

### def order_ready_for_pickup(order)
#### Description:
Places order in pickup queue so it can be delivered by courier. Informs outside world that the order was prepped and is ready.
#### args:
order: {
    id: "ID of order",
    name: "description of order",
    prepTime: "integer value representing the number of seconds to prep the food"
}
#### Returns:
None

### def courier_ready_for_pickup(order)
#### Description:
Places courier in pickup queue so courier can pickup order if ready. Informs outside world that the courier has arrived to pickup order.
#### args:
order: {
    id: "ID of order",
    name: "description of order",
    prepTime: "integer value representing the number of seconds to prep the food"
}
#### Returns:
None

### def pickup_order(order)
#### Description:
Delivers order and removes order and courier from their queues. Informs outside world that the order was pickup by the courier, and statistics of waiting times for food and courier.
#### args:
order: {
    id: "ID of order",
    name: "description of order",
    prepTime: "integer value representing the number of seconds to prep the food"
}
#### Returns:
None

### def finish_cli()
#### Description:
Informs outside world of average food and courier wait times.


## In Designing the system, 3 patterns were used:
### 1. Domain Driven Design 
### 2. Event Driven Architecture
### 3. Test Driven Design

## Domain Driven Design(DDD): 
DDD is useful when tackling a complex problem. When a system has many moving parts, it can beadvantageous to separate the system into each of their categories. The system was separated into 4 components. We have the service, which consists of the event bus and the event handlers(More on this in Event Driven Architecture, below). These services handle the components of sending events when triggered to and handling those events. When an order is made, or an order is ready, or a courier needs to be dispatched, or an order is ready for pickup, we emit those event to the bus, where the handlers for those events are listening and take the appropriate action. The handlers provide the service and means to which our system operates but other parts of the system don't need to be involved with the services that are provided. We also have the adapter, which provides the system a means to communicate with the outside world and allows the system to display the System's current actions. Additionally, we have the domain layer, which contains the business logic, this is where couriers are added to the waiting queue, or where orders are added to the waiting queue. This is where checking if an order is prepared or if a courier has arrived is done. And lastly, we have the entry points to the system. This is the API, where we can communicate with the system. This is where data is given to the system and the sytem will handle the request.

## Event Driven Architecture(EDA): 
This system relies on notifications or events. When an order is being placed, send an Event! When an order is ready, send an event! When a courier has arrived for an order, SEND AN EVENT! The system relies on this Architecture which helps decouple parts of the system. The system only reacts to the events. The system revolves around a courier arriving, or an order being prepped, or an order being placed, and so on. The system reacts to these events and takes the appropriate action.

## Test Driven Development(TDD): 
When developing parts of the system, it’s important to know what each component should do. Using TDD can help ensure each domain stays on its original course and ensure each component functions correctly. The system has clear defined set of expected inputs and outputs. When an order is placed a courier should be dispatched and the outside world should have visibility to the system's actions.

## Design Decisions:
The system was created to run asynchronously. The Kitchen places an order and must wait for the food to cook (Similar to waiting for IO). The time it takes to cook this food shouldn't be spent looking at the food and waiting for it to cook, it should be spent on other tasks like taking other orders, dispatching couriers, checking if a courier's order is ready so he/she can pick it up! Python's Asyncio IO package was used so multiple tasks can run concurrently while other tasks are waiting. The event bus was implemented to add multiple tasks so system can execute these tasks in appropriate order. There are multiple tasks that are running, and if one of those tasks are completed, the system should be notified so it can take the next appropriate action.

The simulator handles all the prep time: waiting for food to be prepped or waiting for the courier to arrive. It did not feel right to have the entry points sleep when it receives these requests, the simulator seemed like the logical solution to handle the sleep. The entry points should just handle the order it receives.




