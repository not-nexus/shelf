import logging
import sys


class LoggerCreator(object):
    """
        The purpose of this class is to create a logger or configure a logger.

        It exists instead of functions because I realized I needed a reference to things
        like the handler in multiple places for different reasons and I didn't want to
        pass them around every time.
    """
    REQUEST_FORMAT = "%(asctime)s - %(levelname)s %(user)s%(request_id)s%(method_and_uri)s- %(message)s"
    BACKGROUND_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

    def __init__(self, logger_or_name=None):
        """
            Args:
                logger_or_name(logging.Logger|string)
        """
        if isinstance(logger_or_name, basestring):
            self.logger = logging.getLogger(logger_or_name)
        else:
            self.logger = logger_or_name

        self.handler = logging.StreamHandler(sys.stdout)
        self.logger.addHandler(self.handler)

    def request_format(self):
        """
            Configures the logger to use a requst format which includes
            things like the "request_id" and the "url".

            IMPORTANT NOTE: This format will not work with the
            shelf.request_log_filter.RequestLogFilter but I cannot
            add it here due to a circular dependency.

            The problem is the logger exists in the app context but
            requires the use of the container stored on the request
            context. The means I need to use the unholy
            shelf.get_container.get_container function which will
            not work because of circular dependencies. See the function
            for more information.

            Returns:
                shelf.logger_creator.LoggerCreator
        """
        self.formatter = logging.Formatter(LoggerCreator.REQUEST_FORMAT)
        self.handler.setFormatter(self.formatter)

        return self

    def background_format(self):
        """
            Configures a logger to use a minimal format which doesn't
            include anything request related.

            Returns:
                shelf.logger_creator.LoggerCreator
        """
        self.formatter = logging.Formatter(LoggerCreator.BACKGROUND_FORMAT)
        self.handler.setFormatter(self.formatter)

        return self

    def level(self, level):
        """
            Sets the log level. This MUST be one of the
            flags assigned on the logging module.

            https://docs.python.org/2/library/logging.html#logging-levels

            Args:
                level(int)

            Returns:
                shelf.logger_creator.LoggerCreator
        """
        self.handler.setLevel(level)
        self.logger.setLevel(level)

        return self

    def level_name(self, level_name):
        """
            Sets the log level based on a name
            such as "DEBUG" or "INFO".

            Args:
                level_name(string)

            Returns:
                shelf.logger_creator.LoggerCreator
        """
        level_name = level_name.upper()
        level = logging.getLevelName(level_name)
        self.level(level)

        return self

    def get(self):
        """
            Gets the logger configured so far.

            Returns:
                logging.Logger
        """
        return self.logger
