import time
import threading
import logging

# Configure logging to save to a file
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Node:
    def __init__(self, node_id, master):
        self.node_id = node_id
        self.load = 0
        self.master = master
        self.resources = set()
        self.processes = []
        self.status = "active"

        self.run_thread = threading.Thread(target=self.run_processes)
        self.run_thread.start()

    def queue_process(self, process):
        if not self.status == "failed" and self.load < 5:
            self.load += 1
            logging.info(f"NODE: Nodo {self.node_id} ha recibido el proceso {process.process_id}. Carga actual: {self.load}")
            self.processes.append(process)
            return True
        return False

    def run_processes(self):
        while self.status == "active":
            if self.processes:
                self.status = "running"
                logging.info(f"NODE: Nodo {self.node_id} está corriendo el proceso {self.processes[0].process_id}")
                self.processes[0].run(self)


    def reset_process(self):
            self.processes[0].reset_process()
            self.status = "reset_process"

    def release_process(self, process):
        if self.status == "reset_process":
            logging.info(f"NODE: # # # RESET: Nodo {self.node_id} ha reiniciado el proceso {process.process_id}. Carga actual: {self.load}")
        else: 
            self.load -= 1
            logging.info(f"NODE: # # # # # COMPLETED: Nodo {self.node_id} ha liberado el proceso {process.process_id}. Carga actual: {self.load}")
            self.processes.remove(process)
            
        resources_list = list(self.resources)
        for resource in resources_list:
            self.release_resource(resource)
        self.status = "active"

    def request_resource(self, resource_id):
        """
        Solicita un recurso al master.
        """
        if self.master.queue_resource(resource_id, self.node_id):
            self.status = "waiting_resource"
            logging.info(f"NODE: Nodo {self.node_id} está en espera para el recurso {resource_id}")
            return True
        return False

    def accept_resource(self, resource_id):
        """
        Acepta un recurso asignado por el master.
        """
        if self.status == "waiting_resource":
            self.resources.add(resource_id)
            self.processes[0].accept_resource(resource_id)
            logging.info(f"NODE: Nodo {self.node_id} ha obtenido el recurso {resource_id}")
        else:
            logging.warning(f"NODE: Nodo {self.node_id} no puede aceptar el recurso {resource_id}")

    def release_resource(self, resource_id):
        """
        Libera un recurso, permitiendo que otros nodos puedan utilizarlo.
        """
        if resource_id in self.resources:
            self.resources.remove(resource_id)
            if self.master.release_resource(resource_id, self.node_id):
                logging.info(f"NODE: Nodo {self.node_id} ha liberado el recurso {resource_id}")
            else:
                logging.warning(f"NODE: Nodo {self.node_id} no ha podido liberar el recurso {resource_id}")

    def detect_failure(self):
        while self.is_active:
            try:
                response = self.master.ping(self)
                if not response:
                    logging.error(f"NODE: Nodo {self.node_id} ha detectado un fallo en el maestro.")
                    self.is_active = False
            except Exception as e:
                logging.error(f"NODE: Nodo {self.node_id} ha detectado un fallo en el maestro.")
                self.is_active = False
            time.sleep(5)