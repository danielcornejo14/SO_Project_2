import threading
from queue import PriorityQueue
from node import Node

class Master:
    def __init__(self, num_nodes, resource_manager):
        # Set the master as running
        self.running = True
        # Create and fill the list of nodes
        self.nodes = [Node(self) for _ in range(num_nodes)]

        # Create a resource manager
        self.resource_manager = resource_manager

        # Create a priority queue to store incoming messages
        self.resource_queue = PriorityQueue()
        self.process_queue

        # start the thread to assign processes to nodes
        self.assign_thread = threading.Thread(target=self.assign_process)
        self.assign_thread.start()

        self.lock = threading.Lock()
    
    def set_process_queue(self, process_queue):
        # Set by the user (allows more control over the examples shown)
        self.process_queue = process_queue

    def assign_process(self):
        while self.running:
            if not self.process_queue.empty():
                _, process = self.process_queue.get()
                # Find the node with the lowest load
                lowest_load_node = min(self.nodes, key=lambda node: node.load)
                lowest_load_node.assign_process(process)

    def assign_resource(self, resource_id):
        """
        Asigna un recurso a un nodo.
        """
        return self.resource_manager.request_resource(resource_id)
    
    def monitor_nodes(self):
        for node in self.nodes:
            status = node.get_status()

    def stop(self):
        self.running = False
        self.server_socket.close()
        self.listen_thread.join()