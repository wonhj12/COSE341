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


def process_worker(worker_id):
    """Function for each worker to process its assigned orders."""
    while True:
        with worker_locks[worker_id]:
            if not worker_queues[worker_id].empty():
                order = worker_queues[worker_id].get()
                print(f"Worker {worker_id} processing order: {order['id']}")

                # Process each item in the order
                for item in order['items']:
                    drink_name = item['item']
                    quantity = item['quantity']

                    for _ in range(quantity):
                        # Check if we have enough ingredients for this drink
                        can_make_drink = True
                        with inventory_lock:
                            for ingredient, required_amount in recipes[drink_name].items():
                                if inventory[ingredient] < required_amount:
                                    print(f"Sold Out! Not enough {ingredient} for {drink_name}")
                                    can_make_drink = False
                                    break

                            # If we can make the drink, reduce inventory
                            if can_make_drink:
                                for ingredient, required_amount in recipes[drink_name].items():
                                    inventory[ingredient] -= required_amount

                        if can_make_drink:
                            # Simulate drink preparation time
                            time.sleep(processing_times[drink_name])
                            print(f"Worker {worker_id} completed {drink_name} for Order {order['id']}")
                        else:
                            # Not enough inventory to make this drink; log and skip
                            break

                print(f"Worker {worker_id} completed Order {order['id']}.")

current_worker_id = 0

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
