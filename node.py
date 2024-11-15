import socket
import json

class Node:
    def __init__(self, master_port):
        self.master_port = master_port

    def send_message_to_master(self, message, priority):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(('127.0.0.1', self.master_port))
                data = json.dumps({'message': message, 'priority': priority})
                s.sendall(data.encode('utf-8'))
        except Exception as e:
            print(f"Error sending message to master: {e}")