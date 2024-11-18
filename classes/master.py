import threading
from .node import Node
from queue import PriorityQueue
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Master:
    def __init__(self, num_nodes, resource_manager):
        # Set the master as running
        self.running = True
        # Create and fill the list of nodes
        self.nodes = [Node(i, self) for i in range(num_nodes)]

        self.process_lock = threading.Lock()
        self.resource_lock = threading.Lock()

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
            with self.process_lock:
                if not self.process_queue.empty():
                    _, process = self.process_queue.get_nowait()
                    # Find the node with the lowest load
                    lowest_load_node = min(self.nodes, key=lambda node: node.load)
                    if not lowest_load_node.queue_process(process):
                        logging.warning(f"MASTER: No hay nodos disponibles para el proceso {process.process_id}")
                        self.process_queue.put((_, process))
                        self.nodes.append(Node(len(self.nodes), self))
                        logging.info(f"MASTER: Se ha creado un nuevo nodo {len(self.nodes) - 1}")

    def queue_resource(self, resource, node_id):
        """
        Guarda la solicitud de un recurso de un nodo en una cola de espera.
        """
        if self.running:
                try:
                    with self.resource_lock:
                        self.resource_queue[node_id] = (resource, time.time())
                        return True
                except:
                    return False
                    
    def assign_resource(self):
        while self.running:
            with self.resource_lock:
                for node_id, resource_req in list(self.resource_queue.items()):
                    if time.time() - resource_req[1] > 5:
                        logging.warning(f"MASTER: Nodo {node_id} ha esperado mucho tiempo por el recurso {resource_req[0]}")
                        self.resource_queue.pop(node_id)
                        self.nodes[node_id].reset_process()
                        continue
                    if self.resource_manager.request_resource(resource_req[0]):
                        self.nodes[node_id].accept_resource(resource_req[0])
                        self.resource_queue.pop(node_id)
                    else:
                        logging.warning(f"MASTER: No hay recurso {resource_req[0]} disponible para el nodo {node_id}")
            time.sleep(1)
    
    def release_resource(self, resource, node_id):
        """
        Libera un recurso de un nodo.
        """
        try:
            with self.resource_lock:
                logging.info(f"MASTER: Liberando recurso {resource} del nodo {node_id}")
                self.resource_manager.release_resource(resource)
                return True
        except:
            return False
    
    def monitor_nodes(self):
        for node in self.nodes:
            return

    def stop(self):
        self.running = False
        self.assign_process_thread.join()
        self.assign_resource_thread.join()
        #self.monitor_thread.join()