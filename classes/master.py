import threading
from .node import Node
from queue import PriorityQueue
import time

class Master:
    def __init__(self, num_nodes, resource_manager):
        # Set the master as running
        self.running = True
        # Create and fill the list of nodes
        self.nodes = [Node(i, self) for i in range(num_nodes)]

        self.lock = threading.Lock()

        # Create a resource manager
        self.resource_manager = resource_manager

        # Create a list and a priority queue to store incoming messages
        self.resource_queue = {}
        self.process_queue = PriorityQueue()

        # start the threads
        self.assign_process_thread = threading.Thread(target=self.assign_process)
        self.assign_process_thread.start()

        self.assign_resource_thread = threading.Thread(target=self.assign_resource)
        self.assign_resource_thread.start()

        #self.monitor_thread = threading.Thread(target=self.monitor_nodes)
        #self.monitor_thread.start()
    
    def set_process_queue(self, process_queue):
        # Set by the user (allows more control over the examples shown)
        self.process_queue = process_queue

    def assign_process(self):
        while self.running:
            if not self.process_queue.empty():
                _, process = self.process_queue.get_nowait()
                # Find the node with the lowest load
                lowest_load_node = min(self.nodes, key=lambda node: node.load)
                lowest_load_node.queue_process(process)

    def queue_resource(self, resource, node_id):
        """
        Asigna un recurso a un nodo.
        """
        if self.running:
            try:
                self.resource_queue[node_id] = resource
                return True
            except:
                return False
                
    def assign_resource(self):
        while self.running:
            with self.lock:
                while self.resource_queue:
                    node_id, resource = next(iter(self.resource_queue.items()))
                    if self.resource_manager.request_resource(resource):
                        self.nodes[node_id].accept_resource(resource)
                        self.resource_queue.pop(node_id)
                time.sleep(1) 
    
    def release_resource(self, resource, node_id):
        """
        Libera un recurso de un nodo.
        """
        with self.lock:
            self.resource_manager.release_resource(resource)
            return True
        return False #failed to release resource
    
    def monitor_nodes(self):
        for node in self.nodes:
            return

    def stop(self):
        self.running = False
        self.assign_thread.join()
        self.assign_resource_thread.join()
        self.monitor_thread.join()