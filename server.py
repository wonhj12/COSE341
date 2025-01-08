from xmlrpc.server import SimpleXMLRPCServer
from threading import Thread, Lock
import queue
import time

# Menu processing times (in seconds)
processing_times = {
    'Americano': 4,
    'Latte': 6,
    'Green Tea Latte': 6,
    'Frappuccino': 10
}

inventory = {
    'Coffee': 100,
    'Milk': 50,
    'Green_Tea': 20,
    'Chocolate': 20,
    'Cream': 15
}

recipes = {
    'Americano':     {'Coffee': 10},
    'Latte':         {'Coffee': 8,  'Milk': 5},
    'Green Tea Latte': {'Green_Tea': 5, 'Milk': 4},
    'Frappuccino':   {'Chocolate': 5, 'Milk': 5, 'Cream': 3}
}

prices = {
    'Americano': 1500,
    'Latte': 3000,
    'Green Tea Latte': 4000,
    'Frappuccino': 5000
}

# Thread-safe order queue
order_queue = queue.Queue()
order_lock = Lock()

# Lock to protect inventory
inventory_lock = Lock()

# Number of worker threads
NUM_WORKERS = 4

# Order queues for each worker
worker_queues = [queue.Queue() for _ in range(NUM_WORKERS)]
worker_locks = [Lock() for _ in range(NUM_WORKERS)]

import time
import queue
from threading import Thread, Lock

# Menu processing times (in seconds)
processing_times = {
    'Americano': 4,
    'Latte': 6,
    'Green Tea Latte': 6,
    'Frappuccino': 10
}

inventory = {
    'Coffee': 100,
    'Milk': 50,
    'Green_Tea': 20,
    'Chocolate': 20,
    'Cream': 15
}

recipes = {
    'Americano': {'Coffee': 10},
    'Latte': {'Coffee': 8, 'Milk': 5},
    'Green Tea Latte': {'Green_Tea': 5, 'Milk': 4},
    'Frappuccino': {'Chocolate': 5, 'Milk': 5, 'Cream': 3}
}

# Thread-safe order queues for each worker
NUM_WORKERS = 4
worker_queues = [queue.Queue() for _ in range(NUM_WORKERS)]
worker_locks = [Lock() for _ in range(NUM_WORKERS)]

# Lock to protect inventory
inventory_lock = Lock()

# Variable to assign orders in a round-robin manner
current_worker_id = 0
order_assign_lock = Lock()  # Lock to protect current_worker_id

profit = 0 # Total profit

def process_worker(worker_id):
    """Function for each worker to process its assigned orders."""
    global profit
    while True:
        try:
            # Wait for an order to be available
            order = worker_queues[worker_id].get(timeout=1)  # Timeout to allow graceful exit
        except queue.Empty:
            continue  # No order to process, continue waiting

        print(f"Worker {worker_id} processing Order {order['id']}")
        order_profit = 0 # Profit for this order

        # Process each item in the order
        for item in order['items']:
            drink_name = item['item']
            quantity = item['quantity']

            for _ in range(quantity):
                # Attempt to make the drink
                can_make_drink = False

                with inventory_lock:
                    # Check if enough ingredients are available
                    can_make_drink = True
                    for ingredient, required_amount in recipes[drink_name].items():
                        if inventory.get(ingredient, 0) < required_amount:
                            print(f"Sold Out! Not enough {ingredient} for {drink_name} in Order {order['id']}")
                            can_make_drink = False
                            break

                    if can_make_drink:
                        # Deduct the ingredients from inventory
                        for ingredient, required_amount in recipes[drink_name].items():
                            inventory[ingredient] -= required_amount
                        print(f"Ingredients reserved for {drink_name} in Order {order['id']}")
                        order_profit += prices[drink_name]

                if can_make_drink:
                    # Simulate drink preparation time
                    time.sleep(processing_times[drink_name])
                    print(f"Worker {worker_id} completed {drink_name} for Order {order['id']}")
                else:
                    # Not enough inventory to make this drink; skip to next item
                    break
        with order_lock:
            profit += order_profit
        print(f"Worker {worker_id} completed Order {order['id']}.")
        print(f"Total profit: {profit}")

def assign_order(order_items):
    """
    Assign an order to a worker in a thread-safe manner using round-robin.
    order_items example: [{'item': 'Americano', 'quantity': 2}, ...]
    """
    global current_worker_id

    order_id = int(time.time() * 1000)
    order = {'id': order_id, 'items': order_items}

    with order_assign_lock:
        worker_id = current_worker_id
        current_worker_id = (current_worker_id + 1) % NUM_WORKERS
        worker_queues[worker_id].put(order)
        print(f"Order {order_id} assigned to Worker {worker_id}.")

    return f"Order {order_id} is being processed by Worker {worker_id}."

def start_workers():
    """Initialize and start all worker threads."""
    for worker_id in range(NUM_WORKERS):
        thread = Thread(target=process_worker, args=(worker_id,), daemon=True)
        thread.start()
        print(f"Worker {worker_id} started.")

# Initialize and start worker threads
start_workers()

def process_order(order_items):
    """
    Add an order to the shared queue and assign to a worker in round-robin manner.
    order_items example: [{'item': 'Americano', 'quantity': 2}, ...]
    """
    global current_worker_id
    
    order_id = int(time.time() * 1000)
    order = {'id': order_id, 'items': order_items}
    
    with order_lock:
        worker_id = current_worker_id
        
        # update worker_id
        current_worker_id = (current_worker_id + 1) % NUM_WORKERS
        worker_queues[worker_id].put(order)
        order_queue.put(order)
        
        print(f"Order {order_id} assigned to Worker {worker_id}.")
    
    return f"Order {order_id} is being processed by Worker {worker_id}."

def main():
    # Create RPC server
    server = SimpleXMLRPCServer(("localhost", 9000), allow_none=True)
    print("RPC Server is running on localhost:9000")
    
    # Register functions
    server.register_function(process_order, "process_order")
    
    # Start worker threads
    for i in range(NUM_WORKERS):
        Thread(target=process_worker, args=(i,), daemon=True).start()
    
    # Run the server's main loop
    server.serve_forever()


if __name__ == "__main__":
    main()
