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

# Thread-safe order queue
order_queue = queue.Queue()
order_lock = Lock()

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
                for item in order['items']:
                    # Process each item in the order
                    for _ in range(item['quantity']):
                        time.sleep(processing_times[item['item']])
                        print(f"Worker {worker_id} completed {item['item']} for Order {order['id']}")
                print(f"Worker {worker_id} completed Order {order['id']}.")


def process_order(order_items):
    """Add an order to the shared queue and assign to a worker."""
    order_id = int(time.time() * 1000)  # Unique ID based on timestamp
    order = {'id': order_id, 'items': order_items}
    
    # Assign order to the next worker in a round-robin manner
    with order_lock:
        worker_id = order_queue.qsize() % NUM_WORKERS  # Round-robin assignment
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
