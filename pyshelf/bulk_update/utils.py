import logging
import os
import sys
import pyshelf.configure as configure
from pyshelf.bulk_update.container import Container
from pyshelf.bulk_update.index_pruner import IndexPruner


def run(args):
    """
        Starts off the whole bulk-update process.

        Args:
            args(dict): A dictionary of arguments and
                options provided to the update-search-index
                script
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
    logger = logging.getLogger("update-search-index")
    logger.addHandler(handler)
    logger.setLevel(log_level)

    config = {
        "logLevel": log_level,
        "chunkSize": int(args["--chunk-size"])
    }

    configure.app_config(config, args["<config-path>"])

    bucket_string = args.get("--bucket")
    bucket_list = []  # heh

    if bucket_string:
        bucket_list = bucket_string.split(",")
        bucket_list = [val.strip() for val in bucket_list]

    container = Container(config, logger)
    container.runner.run(bucket_list)


def run_search_prune(args):
    """
        Runs search cleanup based on given config file.

        Args:
            args(dict)
    """
    log_level = logging.INFO

    if args["--verbose"]:
        log_level = logging.DEBUG

    config = {
        "logLevel": log_level
    }
    configure.app_config(config, args["<config-path>"])

    log_name = "prune-search-index"
    log_file = os.path.join(config["indexPruneLogDirectory"], log_name + ".log")
    handler = logging.FileHandler(log_file)
    logger = logging.getLogger(log_name)
    logger.addHandler(handler)
    logger.setLevel(log_level)

    pruner = IndexPruner(config, logger)
    pruner.run()
