import socket
import threading
import json
from queue import PriorityQueue
from node import Node

class Master:
    def __init__(self, num_nodes, port):
        # Set the master as running
        self.running = True

        # Create and fill the list of nodes
        self.nodes = []
        for i in range(num_nodes):
            self.nodes.append(Node())

        # Create a priority queue to store incoming messages
        self.queue = PriorityQueue()

        # Port and socket to listen for incoming node connections
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('0.0.0.0', self.port))
        self.server_socket.listen(5)

        # start the thread to assign processes to nodes
        #self.assign_process_thread = threading.Thread(target=self.assign_process)
        #self.assign_process_thread.start()

        # Start the thread to listen for incoming connections
        self.listen_thread = threading.Thread(target=self.listen_for_connections)
        self.listen_thread.start()
        
        # Start the thread to read messages
        self.response_thread = threading.Thread(target=self.process_messages)
        self.response_thread.start()

    def listen_for_connections(self):
        while self.running:
            client_socket, addr = self.server_socket.accept()
            self.handle_client(client_socket)

    def handle_client(self, client_socket):
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                data = json.loads(message)
                data['client_socket'] = client_socket  # Add client_socket to the data dictionary
                priority = data.get('priority', 0)
                if priority:
                    self.queue.put((priority, data))
                else:
                    raise ValueError("Invalid priority value")
        except Exception as e:
            print(f"Error handling client: {e}") # TODO logger
            client_socket.close()

    def process_messages(self):
        while self.running:
            if not self.queue.empty():
                priority, message = self.queue.get()
                # Process the message based on its content
                print(f"Processing message with priority {priority}: {message}")

    def stop(self):
        self.running = False
        self.server_socket.close()
        self.listen_thread.join()

    def assign_process(self, process):
        return
    
    def assign_resource(self, resource):
        return
    
    def monitor_nodes(self):
        for node in self.nodes:
            status = node.get_status()

    def parse_status(self, status):
        return

# Example usage
if __name__ == "__main__":
    master = Master(num_nodes=5, port=12345)
    try:
        master.process_messages()
    except KeyboardInterrupt:
        master.stop()