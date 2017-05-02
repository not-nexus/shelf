from shelf.bulk_update.runner import Runner


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

    def create_runner(self, bucket_action):
        """
            Args:
                bucket_action(function):   The action to run on each bucket.

            Returns:
                shelf.bulk_update.runner.Runner
        """
        return Runner(self, bucket_action)

