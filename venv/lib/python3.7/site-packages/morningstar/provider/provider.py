from abc import ABC, abstractmethod


class Provider(ABC):

    @abstractmethod
    def __init__(self, config):
        """
        Args:
            config (dict): dictionary containing configuration parameters
        """
        self.config = config
