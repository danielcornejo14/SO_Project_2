import threading
class Resource_Manager:
    def __init__(self):
        self.resources = {}
        self.lock = threading.Lock()

    def add_resource(self, resource_id):
        with self.lock:
            self.resources[resource_id] = True
    
    def request_resource(self, node, resource_id):
        with self.lock:
            if self.resources.get(resource_id, False):
                self.resources[resource_id] = False
                return True
            return False
    
    def request_resource(self, resource_id):
        with self.lock:
            if self.resources.get(resource_id, False):
                self.resources[resource_id] = False
                return True
            return False
    
    def release_resource(self, resource_id):
        with self.lock:
            if resource_id in self.resources:
                self.resources[resource_id] = True
                return True