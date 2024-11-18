from classes.master import Master
from classes.resource_manager import ResourceManager
from queue import PriorityQueue
from classes.process import Process

def test_1():
    # Create and add resources to the resource manager
    resource_manager = ResourceManager()

    resource_manager.add_resource("R1", 2)
    resource_manager.add_resource("R2", 1)
    resource_manager.add_resource("R3", 3)

    # Create a master node
    master = Master(3, resource_manager)

    # Create processes
    process1 = Process(1, ["R1", "R2"])
    process2 = Process(2, ["R2", "R3"])
    process3 = Process(3, ["R3", "R1"])
    process4 = Process(4, ["R1", "R2", "R3"])

    # Create a priority queue and store the processes
    process_queue = PriorityQueue()

    process_queue.put((1, process1))
    process_queue.put((2, process2))
    process_queue.put((3, process3))
    process_queue.put((4, process4))

    # Set the process queue in the master
    master.set_process_queue(process_queue)

def test_2():
    # Create and add resources to the resource manager
    resource_manager = ResourceManager()

    resource_manager.add_resource("R1", 2)
    resource_manager.add_resource("R2", 1)
    resource_manager.add_resource("R3", 3)

    # Create a master node
    master = Master(3, resource_manager)

    # Create processes
    process1 = Process(1, ["R2", "R1"])
    process2 = Process(2, ["R1", "R2"])
    process3 = Process(3, ["R2", "R1"])
    process4 = Process(4, ["R1", "R2", "R3"])

    # Create a priority queue and store the processes
    process_queue = PriorityQueue()

    process_queue.put((1, process1))
    process_queue.put((2, process2))
    process_queue.put((3, process3))
    process_queue.put((4, process4))

    # Set the process queue in the master
    master.set_process_queue(process_queue)

def test_3():
    # Create and add resources to the resource manager
    resource_manager = ResourceManager()

    resource_manager.add_resource("R1", 2)
    resource_manager.add_resource("R2", 1)
    resource_manager.add_resource("R3", 3)

    # Create a master node
    master = Master(1, resource_manager)

    # Create processes
    process1 = Process(1, ["R2", "R1"])
    process2 = Process(2, ["R1", "R2"])
    process3 = Process(3, ["R2", "R1"])
    process4 = Process(4, ["R1", "R2", "R3"])
    process5 = Process(5, ["R1", "R2"])
    process6 = Process(6, ["R2", "R1"])
    process7 = Process(7, ["R2", "R1"])
    process8 = Process(8, ["R1", "R2", "R3"])

    # Create a priority queue and store the processes
    process_queue = PriorityQueue()

    process_queue.put((1, process1))
    process_queue.put((2, process2))
    process_queue.put((3, process3))
    process_queue.put((4, process4))
    process_queue.put((5, process5))
    process_queue.put((6, process6))
    process_queue.put((7, process7))
    process_queue.put((8, process8))

    # Set the process queue in the master
    master.set_process_queue(process_queue)
# RUN TEST
test_3()