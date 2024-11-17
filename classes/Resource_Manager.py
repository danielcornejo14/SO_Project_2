import threading
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ResourceManager:
    def __init__(self):
        self.resources = {}

    def add_resource(self, resource_id, resource_quantity):
            self.resources[resource_id] = resource_quantity
    
    def request_resource(self, resource_id):
            if self.resources.get(resource_id, 0) > 0:
                self.resources[resource_id] -= 1
                return True
            return False
    
    def release_resource(self, resource_id):
            if resource_id in self.resources:
                self.resources[resource_id] += 1
                logging.info(f"RESOURCE MANAGER: Recurso {resource_id} liberado, cantidad actual: {self.resources[resource_id]}")
                return True
            return False