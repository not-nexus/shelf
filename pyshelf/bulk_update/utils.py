import logging
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
    log_level = logging.INFO

    if args["--verbose"]:
        log_level = logging.DEBUG

    # Important to not use logging.basicConfig here
    # because calling it again (in subprocesses) is
    # a no-op and its easiest to use it in the subprocesses
    # because then it also automatically configures child
    # loggers such as boto and elasticsearch
    handler = logging.StreamHandler(stream=sys.stdout)
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
