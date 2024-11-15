import time
import random

class Process:
    def __init__(self, process_id, resources):
        self.process_id = process_id
        self.resources = resources


    def run(self, node):
        for resource in self.resources:
            time.sleep(random.uniform(0.1, 3.0))
            while not node.request_resource(resource):
                time.sleep(1)
        time.sleep(random.uniform(0.1, 3.0))
        node.release_process(self.process_id)
