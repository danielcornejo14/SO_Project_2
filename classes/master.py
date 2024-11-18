import threading
from .node import Node
from queue import PriorityQueue
import time
import logging
import random

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Master:
    def __init__(self, num_nodes, resource_manager, node_fail_rate = 0):
        # Set the master as running
        self.running = True
        # Create and fill the list of nodes
        self.nodes = [Node(random.randint(1000, 9999), self, node_fail_rate) for i in range(num_nodes)]
        self.process_list_by_node = {}

        self.process_lock = threading.Lock()
        self.resource_lock = threading.Lock()
        self.node_list_lock = threading.Lock()

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

        self.monitor_thread = threading.Thread(target=self.monitor_nodes)
        self.monitor_thread.start()
    
    def set_process_queue(self, process_queue):
        # Set by the user (allows more control over the examples shown)
        self.process_queue = process_queue

    def assign_process(self):
        while self.running:
            with self.process_lock:
                if not self.process_queue.empty():
                    _, process_id, process = self.process_queue.get()
                    # Find the node with the lowest load
                    try:
                        lowest_load_node = min(self.nodes, key=lambda node: node.load)
                        if not lowest_load_node.queue_process(process):
                            with self.node_list_lock:
                                logging.warning(f"MASTER: No hay nodos disponibles para el proceso {process.process_id}")
                                self.process_queue.put((_, process_id, process))
                                id = random.randint(1000, 9999)
                                self.nodes.append(Node(id, self))
                                logging.info(f"MASTER: # NEW NODE: Se ha creado un nuevo nodo {id}")
                        else: 
                            self.process_list_by_node.setdefault(lowest_load_node.node_id, []).append(process)
                    except Exception as e:
                        logging.error(f"MASTER: Error al asignar proceso: {e}")

    def complete_process(self, node_id, process):
        with self.process_lock:
            self.process_list_by_node[node_id].remove(process)
            logging.info(f"MASTER: Proceso {process.process_id} ha sido completado por el nodo {node_id}")

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
                        node = next((node for node in self.nodes if node.node_id == node_id), None)
                        if node:
                            node.reset_process()
                        continue
                    if self.resource_manager.request_resource(resource_req[0]):
                        node = next((node for node in self.nodes if node.node_id == node_id), None)
                        if node:
                            node.accept_resource(resource_req[0])
                            self.resource_queue.pop(node_id)
                        continue

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
        count = 0
        while self.running:
            time.sleep(2) 
            with self.node_list_lock:
                for node in list(self.nodes):  # Iterate over a copy of the list
                    if node.get_status() == "failed":
                        logging.warning(f"MONITOR: # # FAILED: Nodo {node.node_id} ha fallado")
                        # Requeue processes from the failed node
                        for process in self.process_list_by_node.pop(node.node_id, []):
                                self.process_queue.put((1, process.get_process_id(), process))  # Requeue with priority 1
                        self.nodes.remove(node)
                        id = random.randint(1000, 9999)
                        new_node = Node(id, self)
                        self.nodes.append(new_node)
                        logging.info(f"MONITOR: # NEW NODE: Se ha creado un nuevo nodo {id}")
                    elif node.get_status() == "waiting_resource":
                        count += 1
                        if count > 5:
                            logging.warning(f"MONITOR: Nodo {node.node_id} ha esperado mucho tiempo por un recurso")
                            node.reset_process()
                            count = 0


    def stop(self):
        self.running = False
        self.assign_process_thread.join()
        self.assign_resource_thread.join()
        self.monitor_thread.join()