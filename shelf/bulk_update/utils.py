import logging
import sys
import shelf.configure as configure
from shelf.bulk_update.container import Container
from shelf.bucket_update.utils import update_search_index, prune_search_index


def update(args):
    """
        Kicks off updating of the search layer.

        Args:
            args(dict): A dictionary of arguments and
                options provided to the update-search-index
                script
    """
    run(args, "update-search-index", update_search_index)


def prune(args):
    """
        Removes artifacts from the search layer that no longer exist in the
        cloud layer.

        Args:
            args(dict)
    """

    run(args, "prune-search-index", prune_search_index)


def run(args, logger_name, bucket_action):
    """
        The main runner of updating of the search layer.

        Args:
            args(dict)
            logger_name(basestring)
            bucket_action(function)

    """
    logger = set_up_logger("prune-search-index", args)
    config = get_config(args, logger.level)
    bucket_list = get_bucket_list(args)
    container = Container(config, logger)
    runner = container.create_runner(bucket_action)
    runner.run(bucket_list)


def set_up_logger(task_name, args):
    """
        Sets up logging with the task name, and returns the logger.

        Args:
            task_name(basestring): The name of the task that's about to be run.
            args(dict)

        Returns:
            logging.Logger()
    """
    log_level = logging.INFO

    if args["--verbose"]:
        log_level = logging.DEBUG

    # Important to not use logging.basicConfig here
    # because calling it again (in subprocesses) is
    # a no-op and its easiest to use it in the subprocesses
    # because then it also automatically configures child
    # loggers such as boto and elasticsearch
    handler = logging.StreamHandler(sys.stdout)
    logger = logging.getLogger(task_name)
    logger.addHandler(handler)
    logger.setLevel(log_level)

    return logger


def get_config(args, log_level):
    """
        Takes in the args and the current log level, creates a config object,
        sets the shelf app config, and returns the created config object.

        Args:
            args(dict)
            log_level(int)

        Returns:
            dict
    """
    # Default the chunk_size to 20.
    chunk_size = 20

    if args.get("--chunk-size"):
        chunk_size = int(args.get("--chunk-size"))

    config = {
        "logLevel": log_level,
        "chunkSize": chunk_size
    }

    configure.app_config(config, args["<config-path>"])

    return config


def get_bucket_list(args):
    """
        Takes in the program's args and returns a list containing the bucket
        names (if any) to run the task on.

        Args:
            args(dict)

        Returns:
            List(basestring)
    """
    bucket_string = args.get("--bucket")
    bucket_list = []  # heh

    if bucket_string:
        bucket_list = bucket_string.split(",")
        bucket_list = [val.strip() for val in bucket_list]

    return bucket_list
