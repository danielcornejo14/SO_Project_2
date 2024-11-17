import time
import random
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Process:
    def __init__(self, process_id, resources):
        self.process_id = process_id
        self.resources = resources
        self.waiting = False

    def accept_resource(self):
        self.waiting = False

    def run(self, node):
        for resource in self.resources:
            logging.info(f"Proceso {self.process_id} solicita el recurso {resource}")
            time.sleep(random.uniform(0.1, 3.0))
            if node.request_resource(resource):
                logging.info(f"Proceso {self.process_id} está en espera para el recurso {resource}")
                while self.waiting:
                    time.sleep(1)
            else: 
                logging.info(f"Error: Proceso {self.process_id} tuvo un error al solicitar el recurso {resource}")
                break
            logging.info(f"Proceso {self.process_id} ha obtenido el recurso {resource}")
        time.sleep(random.uniform(0.1, 3.0))
        node.release_process(self)
