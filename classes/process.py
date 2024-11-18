import time
import random
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Process:
    def __init__(self, resources):
        self.process_id = random.randint(1000, 9999)
        self.resources = resources
        self.waiting = False
        self.reset = False

    def get_process_id(self):
        return self.process_id

    def accept_resource(self, resource_id):
        self.waiting = False

    def reset_process(self):
        self.reset = True

    def run(self, node):
        for resource in self.resources:
            time.sleep(random.uniform(0.1, 3.0))
            logging.info(f"PROCESS: Proceso {self.process_id} del nodo {node.node_id} solicita el recurso {resource}")
            if node.request_resource(resource):
                self.waiting = True
                while self.waiting:
                    if self.reset:
                        self.reset = False
                        self.waiting = False
                        node.release_process(self)
                        return

                    logging.info(f"PROCESS: Proceso {self.process_id} del nodo {node.node_id} está esperando el recurso {resource}")
                    time.sleep(1)
            else: 
                logging.error(f"PROCESS: Proceso {self.process_id} tuvo un error al solicitar el recurso {resource}")
                break
            logging.info(f"PROCESS: Proceso {self.process_id} del nodo {node.node_id} ha obtenido el recurso {resource}")
        node.release_process(self)
