import threading
class ResourceManager:
    """
    Potencialmente usada por la clase Master para manejar los recursos.
    """
    def __init__(self):
        self.resources = {}
        self.lock = threading.Lock()

    def add_resource(self, resource_id, resource_quantity):
        with self.lock:
            self.resources[resource_id] = resource_quantity
    
    def request_resource(self, resource_id):
        with self.lock:
            if self.resources.get(resource_id, 0) > 0:
                self.resources[resource_id] -= 1
                return True
            return False
    
    def release_resource(self, resource_id):
        with self.lock:
            if self.resources.get(resource_id, 0):
                self.resources[resource_id] += 1
                return True
            return False