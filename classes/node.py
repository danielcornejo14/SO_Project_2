import time
import threading

class Node:
    def __init__(self, node_id, master):
        self.node_id = node_id
        self.load = 0
        self.master = master
        self.resources = set()
        self.is_active = True
        self.lock = threading.Lock()
    
    def assign_process(self, process_id):
        with self.lock:
            self.load += 1
            print(f"Nodo {self.node_id} ha recibido el proceso {process_id}. Carga actual: {self.load}")
    
    def release_process(self, process_id):
        with self.lock:
            self.load -= 1
            print(f"Nodo {self.node_id} ha liberado el proceso {process_id}. Carga actual: {self.load}")

    def request_resource(self, resource_id):
        """
        Solicita un recurso al master.
        El master debe de tener un método assign_resource que permita asignar un recurso a un nodo.
        """
        success = self.master.assign_resource(self, resource_id)
        if success:
            with self.lock:
                self.resources.add(resource_id)
                print(f"Nodo {self.node_id} ha obtenido el recurso {resource_id}")
        else:
            print(f"Nodo {self.node_id} está en espera para el recurso {resource_id}")

    def release_resource(self, resource_id):
        """
        Libera un recurso, permitiendo que otros nodos puedan utilizarlo.
        El master debe de tener un método release_resource que permita recibir un recurso liberado por un nodo.
        """
        with self.lock:
            if resource_id in self.resources:
                self.resources.remove(resource_id)
                self.master.release_resource(resource_id)
                print(f"Nodo {self.node_id} ha liberado el recurso {resource_id}")

    def detect_failure(self):
        while self.is_active:
            try:
                response = self.master.ping(self)
                if not response:
                    print(f"Nodo {self.node_id} ha detectado un fallo en el maestro.")
                    self.is_active = False
            except Exception as e:
                print(f"Nodo {self.node_id} ha detectado un fallo en el maestro.")
                self.is_active = False
            time.sleep(5)
