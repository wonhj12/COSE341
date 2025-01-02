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
lock = Lock()

# Worker thread function
def process_orders():
    while True:
        with lock:
            if not order_queue.empty():
                order = order_queue.get()
                print(f"Processing order: {order}")
                for item in order['items']:
                    # Simulate Round Robin processing
                    for _ in range(item['quantity']):
                        time.sleep(processing_times[item['item']])
                        print(f"Completed {item['item']} for Order {order['id']}")
                print(f"Order {order['id']} completed.")

# Add order to queue
def process_order(order_items):
    order_id = int(time.time() * 1000)  # Unique ID based on timestamp
    order = {'id': order_id, 'items': order_items}
    order_queue.put(order)
    print(f"Order {order_id} received.")
    return f"Order {order_id} is being processed."

# Main function
def main():
    # Create server object
    server = SimpleXMLRPCServer(("localhost", 9000), allow_none=True)
    print("RPC Server is running on localhost:9000")

    # Register functions
    server.register_function(process_order, "process_order")

    # Start worker threads
    for _ in range(4):
        Thread(target=process_orders, daemon=True).start()

    # Run the server's main loop
    server.serve_forever()

if __name__ == "__main__":
    main()
