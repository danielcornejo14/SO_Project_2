import threading
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class ResourceManager:
    """
    A class to manage resources in a system.
    Attributes:
    -----------
    resources : dict
        A dictionary to store resource IDs and their quantities.
    """

    def __init__(self):
        """
        Initializes the Resource_Manager class.
        This constructor initializes an empty dictionary to store resources.
        """

        self.resources = {}

    def get_resources(self):
        return self.resources

    def add_resource(self, resource_id, resource_quantity):
        """
        Adds a resource to the resource manager.
        Args:
            resource_id (str): The unique identifier for the resource.
            resource_quantity (int): The quantity of the resource to be added.
        Returns:
            None
        """

        self.resources[resource_id] = resource_quantity

    def request_resource(self, resource_id):
        """
        Requests a resource by its ID.
        This method checks if the specified resource is available (i.e., its count is greater than 0).
        If the resource is available, it decrements the resource count by 1 and returns True.
        If the resource is not available, it returns False.
        Args:
            resource_id (int): The ID of the resource to request.
        Returns:
            bool: True if the resource was successfully requested, False otherwise.
        """

        if self.resources.get(resource_id, 0) > 0:
            self.resources[resource_id] -= 1
            return True
        return False

    def release_resource(self, resource_id):
        """
        Releases a resource by incrementing its count in the resource manager.
        Args:
            resource_id (str): The identifier of the resource to be released.
        Returns:
            bool: True if the resource was successfully released, False if the resource_id was not found.
        Logs:
            Logs an info message indicating the resource has been released and the current count of the resource.
        """

        if resource_id in self.resources:
            self.resources[resource_id] += 1
            logging.info(
                f"RESOURCE MANAGER: Recurso {resource_id} liberado, cantidad actual: {self.resources[resource_id]}"
            )
            return True
        return False
