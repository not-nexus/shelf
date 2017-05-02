import logging
import sys
import shelf.configure as configure
from shelf.bulk_update.container import Container
from shelf.bucket_update.utils import update_search_index
from shelf.bucket_update.utils import prune_search_index


def run(args):
    """
        Starts off the whole bulk-update process.

        Args:
            args(dict): A dictionary of arguments and
                options provided to the update-search-index
                script
    """
    logger = set_up_logger("update-search-index", args)
    config = get_config(args, logger.level)
    bucket_list = get_bucket_list(args)
    container = Container(config, logger)
    runner = container.create_runner(update_search_index)
    runner.run(bucket_list)


def run_search_prune(args):
    """
        Runs search pruning based on given config file.

        Args:
            args(dict)
    """
    logger = set_up_logger("prune-search-index", args)
    config = get_config(args, logger.level)
    bucket_list = get_bucket_list(args)
    container = Container(config, logger)
    runner = container.create_runner(prune_search_index)
    runner.run(bucket_list)


def set_up_logger(task_name, args):
    """
        Sets up logging with the task name, and returns the logger.

        Args:
            task_name(basestring): The name of the task that's about to be run.
            args(dict)

        Returns:
            RootLogger()
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
