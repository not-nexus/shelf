import logging


class NullHandler(logging.Handler):
    """
        A handler that does nothing.  Its if I want to make a logger
        that doesn't log anything.
    """
    def emit(self, record):
        """
            Args:
                record(logging.LogRecord): Record to log.  I ignore it.
        """
        pass
