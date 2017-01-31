from shelf.hook.manager import Manager
from shelf.hook.null_manager import NullManager
import multiprocessing


class Container(object):
    def __init__(self, logger):
        """
            Args:
                logger(logging.Logger)
                command(string)
        """
        self.logger = logger

    def create_manager(self, host, command=None):
        """
            Args:
                host(string)
                command(string)

            Returns:
                shelf.hook.manager.Manager
        """
        return Manager(
            self,
            multiprocessing,
            host,
            command
        )

    def create_null_manager(self):
        """
            Returns:
                shelf.hook.null_manager.NullManager
        """
        return NullManager()
