from pyshelf.bulk_update.runner import Runner
from pyshelf.bulk_update.cleaner import Cleaner


class Container(object):
    """
        The goal of this object is to create as little
        objects as possible in order to provide functionality
        for a bulk update of metadata.
    """
    def __init__(self, config, logger):
        """
            Args:
                config(dict): The configuration file decoded
                logger(logging.Logger)
        """
        self.config = config
        self.logger = logger

        self._runner = None
        self._cleaner = None

    @property
    def runner(self):
        """
            Returns:
                pyshelf.bulk_update.runner.Runner
        """
        if not self._runner:
            self._runner = Runner(self)

        return self._runner

    @property
    def cleaner(self):
        """
            Returns:
                pyshelf.bulk_update.cleaner.Cleaner
        """
        if not self._cleaner:
            self._cleaner = Cleaner(self)

        return self._cleaner
