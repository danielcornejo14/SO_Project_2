import threading
from .node import Node
from queue import PriorityQueue
import time
import logging
import random

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Master:
    """The Master class is responsible for managing nodes, processes, and resources in a distributed system."""

    def __init__(self, num_nodes, resource_manager, node_fail_rate = 0):
        """
        Initializes the Master class.
        Args:
            num_nodes (int): The number of nodes to create.
            resource_manager (ResourceManager): The resource manager instance to manage resources.
            node_fail_rate (float, optional): The failure rate of nodes. Defaults to 0.
        Attributes:
            running (bool): Indicates if the master is running.
            nodes (list): A list of Node instances.
            process_list_by_node (dict): A dictionary to store processes by node.
            process_lock (threading.Lock): A lock for process operations.
            resource_lock (threading.Lock): A lock for resource operations.
            node_list_lock (threading.Lock): A lock for node list operations.
            resource_manager (ResourceManager): The resource manager instance.
            resource_queue (dict): A dictionary to store incoming resource messages.
            process_queue (PriorityQueue): A priority queue to store incoming processes.
            assign_process_thread (threading.Thread): A thread to assign processes to nodes.
            assign_resource_thread (threading.Thread): A thread to assign resources to nodes.
            monitor_thread (threading.Thread): A thread to monitor the status of nodes.
        """

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
        """
        Sets the process queue for the master class.
        This method allows the user to set the process queue, providing more control
        over the examples shown.
        Args:
            process_queue (list): A list of processes to be set as the process queue.
        """

        # Set by the user (allows more control over the examples shown)
        self.process_queue = process_queue

    def assign_process(self):
        """
        Assigns processes from the process queue to the node with the lowest load.
        This method continuously checks if there are processes in the process queue
        and assigns them to the node with the lowest load. If no nodes are available
        to handle the process, a new node is created and added to the list of nodes.
        The method ensures thread-safety by using locks when accessing shared resources
        such as the process queue and the list of nodes.
        Raises:
            Exception: If an error occurs while assigning a process to a node.
        Logging:
            Logs warnings if no nodes are available for a process.
            Logs information when a new node is created.
            Logs errors if an exception occurs during process assignment.
        """

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
        """
        Completes the given process on the specified node.
        This method removes the process from the process list of the specified node
        and logs the completion of the process.
        Args:
            node_id (int): The ID of the node where the process is completed.
            process (Process): The process object that has been completed.
        Returns:
            None
        """

        with self.process_lock:
            self.process_list_by_node[node_id].remove(process)
            logging.info(f"MASTER: Proceso {process.process_id} ha sido completado por el nodo {node_id}")

    def queue_resource(self, resource, node_id):
        """
        Adds a resource to the resource queue for a specific node.
        Args:
            resource: The resource to be queued.
            node_id: The identifier of the node for which the resource is being queued.
        Returns:
            bool: True if the resource was successfully queued, False otherwise.
        Raises:
            Exception: If an error occurs while trying to queue the resource.
        """

        if self.running:
                try:
                    with self.resource_lock:
                        self.resource_queue[node_id] = (resource, time.time())
                        return True
                except:
                    return False
                    
    def assign_resource(self):
        """
        Assigns resources to nodes from the resource queue.
        This method continuously checks the resource queue and attempts to assign resources to nodes.
        If a node has been waiting for a resource for more than 5 seconds, a warning is logged, and the node's request is removed from the queue.
        If a resource is available, it is assigned to the node, and the node's request is removed from the queue.
        If a resource is not available, a warning is logged.
        The method uses a lock to ensure thread safety when accessing the resource queue.
        Attributes:
            self.running (bool): A flag indicating whether the resource assignment process should continue running.
            self.resource_lock (threading.Lock): A lock to ensure thread-safe access to the resource queue.
            self.resource_queue (dict): A dictionary where keys are node IDs and values are tuples containing the resource requested and the time of the request.
            self.nodes (list): A list of node objects.
            self.resource_manager (ResourceManager): An object responsible for managing resources.
        Logs:
            Warning messages if a node has waited too long for a resource or if a resource is not available.
        """

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
        Releases a specified resource from a given node.
        This method attempts to release a resource identified by `resource` from the node identified by `node_id`.
        It logs the release action and uses a resource lock to ensure thread safety.
        Args:
            resource (str): The identifier of the resource to be released.
            node_id (int): The identifier of the node from which the resource is being released.
        Returns:
            bool: True if the resource was successfully released, False otherwise.
        """

        try:
            with self.resource_lock:
                logging.info(f"MASTER: Liberando recurso {resource} del nodo {node_id}")
                self.resource_manager.release_resource(resource)
                return True
        except:
            return False
    
    def monitor_nodes(self):
        """
        Monitors the status of nodes in the system and handles node failures.
        This method runs in a loop while the `self.running` flag is True. It performs the following tasks:
        1. Sleeps for 2 seconds between iterations to reduce CPU usage.
        2. Acquires a lock on the node list to ensure thread safety.
        3. Iterates over a copy of the node list to check the status of each node.
        4. If a node has failed:
            a. Logs a warning message indicating the node failure.
            b. Requeues processes from the failed node with priority 1.
            c. Removes the failed node from the node list.
            d. Creates a new node with a random ID and adds it to the node list.
            e. Logs an informational message indicating the creation of the new node.
        """

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

    def stop(self):
        """
        Stops the execution of the master process by setting the running flag to False
        and joining the associated threads to ensure they have completed.
        This method performs the following actions:
        1. Sets the `running` attribute to False to signal the process to stop.
        2. Waits for the `assign_process_thread` to finish execution.
        3. Waits for the `assign_resource_thread` to finish execution.
        4. Waits for the `monitor_thread` to finish execution.
        """

        self.running = False
        self.assign_process_thread.join()
        self.assign_resource_thread.join()
        self.monitor_thread.join()