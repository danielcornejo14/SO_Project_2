import time
from classes.master import Master
from classes.resource import ResourceManager
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
    process1 = Process(["R1", "R2"])
    process2 = Process(["R2", "R3"])
    process3 = Process(["R3", "R1"])
    process4 = Process(["R1", "R2", "R3"])

    # Create a priority queue and store the processes
    process_queue = PriorityQueue()

    process_queue.put((1, process1.get_process_id(), process1))
    process_queue.put((2, process2.get_process_id(), process2))
    process_queue.put((3, process3.get_process_id(), process3))
    process_queue.put((4, process4.get_process_id(), process4))

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
    process1 = Process(["R2", "R1"])
    process2 = Process(["R1", "R2"])
    process3 = Process(["R2", "R1"])
    process4 = Process(["R1", "R2", "R3"])

    # Create a priority queue and store the processes
    process_queue = PriorityQueue()

    process_queue.put((1, process1.get_process_id(), process1))
    process_queue.put((2, process2.get_process_id(), process2))
    process_queue.put((3, process3.get_process_id(), process3))
    process_queue.put((4, process4.get_process_id(), process4))

    # Set the process queue in the master
    master.set_process_queue(process_queue)


def test_3():
    # Create and add resources to the resource manager
    resource_manager = ResourceManager()

    resource_manager.add_resource("R1", 2)
    resource_manager.add_resource("R2", 1)
    resource_manager.add_resource("R3", 3)

    # Create a master node
    master = Master(1, resource_manager, 10)

    # Create processes
    process1 = Process(["R2", "R1"])
    process2 = Process(["R1", "R2"])
    process3 = Process(["R2", "R1"])
    process4 = Process(["R1", "R2", "R3"])

    # Create a priority queue and store the processes
    process_queue = PriorityQueue()

    process_queue.put((1, process1.get_process_id(), process1))
    process_queue.put((1, process2.get_process_id(), process2))
    process_queue.put((3, process3.get_process_id(), process3))
    process_queue.put((4, process4.get_process_id(), process4))

    # Set the process queue in the master
    master.set_process_queue(process_queue)


def test_4():
    # Create and add resources to the resource manager
    resource_manager = ResourceManager()

    resource_manager.add_resource("R1", 2)
    resource_manager.add_resource("R2", 2)
    resource_manager.add_resource("R3", 3)
    resource_manager.add_resource("R4", 3)

    # Create a master node
    master = Master(1, resource_manager)

    # Create processes
    process1 = Process(["R2", "R1", "R4"])
    process2 = Process(["R1", "R2"])
    process3 = Process(["R2", "R1"])
    process4 = Process(["R4", "R2", "R3"])
    process5 = Process(["R1", "R2"])
    process6 = Process(["R2", "R4"])

    # Create a priority queue and store the processes
    process_queue = PriorityQueue()

    process_queue.put((1, process1.get_process_id(), process1))
    process_queue.put((2, process2.get_process_id(), process2))
    process_queue.put((3, process3.get_process_id(), process3))
    process_queue.put((4, process4.get_process_id(), process4))
    process_queue.put((5, process5.get_process_id(), process5))
    process_queue.put((6, process6.get_process_id(), process6))

    # Set the process queue in the master
    master.set_process_queue(process_queue)


def test_5():
    # Create and add resources to the resource manager
    resource_manager = ResourceManager()

    resource_manager.add_resource("R1", 2)
    resource_manager.add_resource("R2", 1)
    resource_manager.add_resource("R3", 3)
    resource_manager.add_resource("R4", 3)
    resource_manager.add_resource("R5", 3)

    # Create a master node
    master = Master(3, resource_manager)

    # Create processes
    process1 = Process(["R2", "R1", "R4", "R5", "R3"])
    process2 = Process(["R1", "R2", "R3", "R4", "R5"])
    process3 = Process(["R2", "R1", "R3", "R4", "R5"])
    process4 = Process(["R1", "R2", "R3", "R4", "R5"])
    process5 = Process(["R1", "R2", "R3", "R4", "R5"])
    process6 = Process(["R2", "R1", "R3", "R4", "R5"])

    # Create a priority queue and store the processes
    process_queue = PriorityQueue()

    process_queue.put((1, process1.get_process_id(), process1))
    process_queue.put((2, process2.get_process_id(), process2))
    process_queue.put((3, process3.get_process_id(), process3))
    process_queue.put((4, process4.get_process_id(), process4))
    process_queue.put((5, process5.get_process_id(), process5))
    process_queue.put((6, process6.get_process_id(), process6))

    # Set the process queue in the master
    master.set_process_queue(process_queue)


def use_case_1():
    # Crear recursos y nodos
    resource_manager = ResourceManager()
    resource_manager.add_resource("R1", 2)
    resource_manager.add_resource("R2", 1)
    resource_manager.add_resource("R3", 3)

    # Crear nodos
    master = Master(3, resource_manager)

    # Crear procesos
    process1 = Process(["R1"])
    process2 = Process(["R2"])
    process3 = Process(["R1", "R2"])
    process4 = Process(["R3"])
    process5 = Process(["R1", "R2", "R3"])

    # Crear cola de procesos
    process_queue = PriorityQueue()
    process_queue.put((1, process1.get_process_id(), process1))
    process_queue.put((2, process2.get_process_id(), process2))
    process_queue.put((3, process3.get_process_id(), process3))
    process_queue.put((4, process4.get_process_id(), process4))
    process_queue.put((5, process5.get_process_id(), process5))

    # Asignar cola de procesos al maestro
    master.set_process_queue(process_queue)
    time.sleep(10)
    master.stop()


def use_case_2():
    # Crear recursos y nodos
    resource_manager = ResourceManager()
    resource_manager.add_resource("R1", 1)

    # Crear nodos
    master = Master(2, resource_manager)

    # Crear procesos
    process1 = Process(["R1"])
    process2 = Process(["R1", "R1"])

    # Crear cola de procesos
    process_queue = PriorityQueue()
    process_queue.put((1, process1.get_process_id(), process1))
    process_queue.put((3, process2.get_process_id(), process2))

    # Asignar cola de procesos al maestro
    master.set_process_queue(process_queue)
    time.sleep(10)
    master.stop()


def use_case_3():
    # Crear recursos y nodos
    resource_manager = ResourceManager()
    resource_manager.add_resource("R1", 3)
    resource_manager.add_resource("R2", 3)

    # Crear nodos
    master = Master(3, resource_manager, 4)

    # Crear procesos
    process1 = Process(["R1"])
    process2 = Process(["R2"])
    process3 = Process(["R1", "R2"])
    process4 = Process(["R1", "R2"])
    process5 = Process(["R1"])

    # Crear cola de procesos
    process_queue = PriorityQueue()
    process_queue.put((1, process1.get_process_id(), process1))
    process_queue.put((2, process2.get_process_id(), process2))
    process_queue.put((3, process3.get_process_id(), process3))
    process_queue.put((4, process4.get_process_id(), process4))
    process_queue.put((5, process5.get_process_id(), process5))

    # Asignar cola de procesos al maestro
    master.set_process_queue(process_queue)
    time.sleep(10)
    master.stop()


def use_case_4():
    # Crear recursos y nodos
    resource_manager = ResourceManager()
    resource_manager.add_resource("R1", 3)
    resource_manager.add_resource("R2", 3)

    # Crear nodos
    master = Master(1, resource_manager)

    # Crear procesos
    process1 = Process(["R1"])
    process2 = Process(["R2"])
    process3 = Process(["R1", "R2"])
    process4 = Process(["R1", "R2"])
    process5 = Process(["R1"])
    process6 = Process(["R2"])
    process7 = Process(["R1", "R2"])

    # Crear cola de procesos
    process_queue = PriorityQueue()
    process_queue.put((1, process1.get_process_id(), process1))
    process_queue.put((2, process2.get_process_id(), process2))
    process_queue.put((3, process3.get_process_id(), process3))
    process_queue.put((4, process4.get_process_id(), process4))
    process_queue.put((5, process5.get_process_id(), process5))
    process_queue.put((6, process6.get_process_id(), process6))
    process_queue.put((7, process7.get_process_id(), process7))

    # Asignar cola de procesos al maestro
    master.set_process_queue(process_queue)
    time.sleep(5)


def use_case_4():
    # Crear recursos y nodos iniciales
    resource_manager = ResourceManager()
    resource_manager.add_resource("R1", 2)
    resource_manager.add_resource("R2", 2)
    master = Master(2, resource_manager)

    # Crear procesos iniciales
    process1 = Process(["R1"])
    process2 = Process(["R2"])
    process_queue = PriorityQueue()
    process_queue.put((1, process1.get_process_id(), process1))
    process_queue.put((2, process2.get_process_id(), process2))
    master.set_process_queue(process_queue)

    # Agregar nuevos nodos dinámicamente
    master.add_node()
    master.add_node()
    time.sleep(10)

    # Verificar que los nodos están integrados
    master.stop()


def use_case_5():
    # Crear recursos y nodos
    resource_manager = ResourceManager()
    resource_manager.add_resource("R1", 3)
    resource_manager.add_resource("R2", 3)

    # Crear nodos
    master = Master(3, resource_manager, 4)

    # Crear procesos
    process1 = Process(["R1"])
    process2 = Process(["R2"])
    process3 = Process(["R1", "R2"])
    process4 = Process(["R1", "R2"])
    process5 = Process(["R1"])

    # Crear cola de procesos
    process_queue = PriorityQueue()
    process_queue.put((1, process1.get_process_id(), process1))
    process_queue.put((2, process2.get_process_id(), process2))
    process_queue.put((3, process3.get_process_id(), process3))
    process_queue.put((4, process4.get_process_id(), process4))
    process_queue.put((5, process5.get_process_id(), process5))

    # Asignar cola de procesos al maestro
    master.set_process_queue(process_queue)
    time.sleep(10)
    master.stop()


use_case_1()
