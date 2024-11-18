import time
import threading
import logging
import random

# Configure logging to save to a file
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Node:
    """Represents a node in a distributed system that can process tasks, manage resources, and handle failures.
    Attributes:
        node_id (int): Unique identifier for the node.
        load (int): Current load of the node, representing the number of processes it is handling.
        fail_rate (int): Probability of node failure during process execution.
        master (object): Reference to the master controller managing the nodes.
        resources (set): Set of resources currently held by the node.
        processes (list): List of processes queued for execution on the node.
        status (str): Current status of the node (e.g., "active", "failed", "running", "reset_process").
        run_thread (threading.Thread): Thread responsible for running processes on the node.
    """

    def __init__(self, node_id, master, fail_rate = 0):
        """
        Initializes a Node instance.
        Args:
            node_id (int): Unique identifier for the node.
            master (object): Reference to the master node or controller.
            fail_rate (float, optional): Probability of node failure. Defaults to 0.
        Attributes:
            node_id (int): Unique identifier for the node.
            load (int): Current load on the node. Defaults to 0.
            fail_rate (float): Probability of node failure.
            master (object): Reference to the master node or controller.
            resources (set): Set of resources managed by the node.
            processes (list): List of processes running on the node.
            status (str): Current status of the node. Defaults to "active".
            run_thread (threading.Thread): Thread to run node processes.
        """

        self.node_id = node_id
        self.load = 0
        self.fail_rate = fail_rate
        self.master = master
        self.resources = set()
        self.processes = []
        self.status = "active"

        self.run_thread = threading.Thread(target=self.run_processes)
        self.run_thread.start()

    def get_status(self):
        """
        Retrieve the current status of the node.
        Returns:
            str: The status of the node.
        """
        return self.status

    def queue_process(self, process):
        """
        Attempts to queue a process to the node if the node is not failed and its load is less than 5.
        Parameters:
        process (Process): The process to be queued.
        Returns:
        bool: True if the process was successfully queued, False otherwise.
        Logs:
        Logs an info message indicating the node ID, process ID, and the current load if the process is successfully queued.
        """

        if not self.status == "failed" and self.load < 5:
            self.load += 1
            logging.info(f"NODE: Nodo {self.node_id} ha recibido el proceso {process.process_id}. Carga actual: {self.load}")
            self.processes.append(process)
            return True
        return False

    def run_processes(self):
        """
        Executes processes assigned to the node while the node status is "active".
        This method continuously checks if the node's status is "active". If there are processes in the node's queue,
        it sets the node's status to "running" and logs the process execution. It generates a random integer to simulate
        the possibility of a node failure. If the random integer is less than or equal to the node's fail rate, the node's
        status is set to "failed" and an error is logged. Otherwise, it runs the first process in the queue.
        Attributes:
            status (str): The current status of the node (e.g., "active", "running", "failed").
            processes (list): A list of processes assigned to the node.
            node_id (int): The unique identifier of the node.
            fail_rate (int): The failure rate of the node, used to determine the likelihood of failure.
        """

        while self.status == "active":
            if self.processes:
                self.status = "running"
                logging.info(f"NODE: Nodo {self.node_id} está corriendo el proceso {self.processes[0].process_id}")
                random_int = random.randint(1, 10)
                if random_int <= self.fail_rate:
                    self.status = "failed"
                    logging.error(f"NODE: Nodo {self.node_id} ha fallado. Estado actual: {self.status}")
                    return
                self.processes[0].run(self)


    def reset_process(self):
            """
            Resets the first process in the processes list and updates the node's status.
            This method calls the reset_process method on the first process in the 
            processes list and sets the node's status to "reset_process".
            """
            
            self.processes[0].reset_process()
            self.status = "reset_process"

    def release_process(self, process):
        """
        Releases a process from the node and updates the node's status and load.
        If the node's status is "reset_process", it logs that the node has reset the process.
        Otherwise, it decreases the node's load by 1, logs that the process has been completed,
        removes the process from the node's process list, and notifies the master that the process
        has been completed.
        Additionally, it releases all resources associated with the node and sets the node's status to "active".
        Args:
            process (Process): The process to be released from the node.
        """

        if self.status == "reset_process":
            logging.info(f"NODE: # # # RESET: Nodo {self.node_id} ha reiniciado el proceso {process.process_id}. Carga actual: {self.load}")
        else: 
            self.load -= 1
            logging.info(f"NODE: # # # # # COMPLETED: Nodo {self.node_id} ha liberado el proceso {process.process_id}. Carga actual: {self.load}")
            self.processes.remove(process)
            self.master.complete_process(self.node_id, process)
            
        resources_list = list(self.resources)
        for resource in resources_list:
            self.release_resource(resource)
        self.status = "active"

    def request_resource(self, resource_id):
        """
        Requests a resource for the node.
        This method attempts to queue a resource request for the node. If the request is successfully queued,
        the node's status is updated to "waiting_resource" and a log entry is created indicating that the node
        is waiting for the specified resource.
        Args:
            resource_id (int): The ID of the resource being requested.
        Returns:
            bool: True if the resource request was successfully queued, False otherwise.
        """
        
        if self.master.queue_resource(resource_id, self.node_id):
            self.status = "waiting_resource"
            logging.info(f"NODE: Nodo {self.node_id} está en espera para el recurso {resource_id}")
            return True
        return False

    def accept_resource(self, resource_id):
        """
        Accepts a resource for the node if it is in the "waiting_resource" status.
        This method checks if the node's status is "waiting_resource". If true, it adds the 
        resource to the node's resources, passes the resource to the first process in the 
        node's processes list, and logs an info message indicating the resource has been 
        obtained. If the node is not in the "waiting_resource" status, it logs a warning 
        message indicating the resource cannot be accepted.
        Args:
            resource_id (int): The ID of the resource to be accepted.
        """

        if self.status == "waiting_resource":
            self.resources.add(resource_id)
            self.processes[0].accept_resource(resource_id)
            logging.info(f"NODE: Nodo {self.node_id} ha obtenido el recurso {resource_id}")
        else:
            logging.warning(f"NODE: Nodo {self.node_id} no puede aceptar el recurso {resource_id}")

    def release_resource(self, resource_id):
        """
        Releases a resource identified by resource_id from the node's resources.
        This method removes the resource from the node's list of resources and 
        attempts to release it through the master. It logs the success or failure 
        of the release operation.
        Args:
            resource_id (int): The identifier of the resource to be released.
        Returns:
            None
        """

        if resource_id in self.resources:
            self.resources.remove(resource_id)
            if self.master.release_resource(resource_id, self.node_id):
                logging.info(f"NODE: Nodo {self.node_id} ha liberado el recurso {resource_id}")
            else:
                logging.warning(f"NODE: Nodo {self.node_id} no ha podido liberar el recurso {resource_id}")