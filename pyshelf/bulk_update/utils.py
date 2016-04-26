import logging
import os
import sys
import pyshelf.configure as configure
from pyshelf.bulk_update.container import Container


def run(args):
    """
        Starts off the whole bulk-update process.

        Args:
            args(dict): A dictionary of arguments and
                options provided to the update-search-index
                script
    """
    container = _configure(args, "update-search-index")
    bucket_string = args.get("--bucket")
    bucket_list = []  # heh

    if bucket_string:
        bucket_list = bucket_string.split(",")
        bucket_list = [val.strip() for val in bucket_list]

    container.runner.run(bucket_list)


def run_clean(args):
    """
        Kicks off cleaning process of search index.

        Args:
            args(dict)
    """
    container = _configure(args, "clean-search-index")
    container.cleaner.run()


def _configure(args, logger_name):
    """
        Configures app, logger, and pyshelf.bulk_update.container.Container.

        Args:
            args(dict)
            logger_name(string)
            file_name(string | None)

        Returns:
            pyshelf.bulk_update.container.Container
    """
    log_level = logging.INFO

    if args["--verbose"]:
        log_level = logging.DEBUG

    # Important to not use logging.basicConfig here
    # because calling it again (in subprocesses) is
    # a no-op and its easiest to use it in the subprocesses
    # because then it also automatically configures child
    # loggers such as boto and elasticsearch
    handler = _get_logging_handler(logger_name, args.get("--log-directory"))
    logger = logging.getLogger(logger_name)
    logger.addHandler(handler)
    logger.setLevel(log_level)

    config = {
        "logLevel": log_level
    }

    if args.get("--chunk-size"):
        config["chunkSize"] = int(args["--chunk-size"])

    configure.app_config(config, args["<config-path>"])
    container = Container(config, logger)

    return container


def _get_logging_handler(logger_name, directory=None):
    """
        Configures logger handler. Creates a logging.FileHandler if directory is given
        or a logging.StreamHandler if directory not given.

        Args:
            logger_name(string)
            directory(string | None): Log output directory
    """
    handler = None

    if directory is not None:
        file_name = os.path.join(directory, logger_name + ".log")
        handler = logging.FileHandler(file_name)
        formatter = logging.Formatter(fmt="%(asctime)s:%(name)s:%(levelname)s:%(message)s")
        handler.setFormatter(formatter)
    else:
        handler = logging.StreamHandler(sys.stdout)

    return handler
