#!/usr/bin/env python
import docopt
import logging
import sys
import pyshelf.configure as configure
from pyshelf.bulk_update.container import Container

doc = """Usage: ./build-cf [options] <config-path>

    Options:
        -b --bucket bucket          The name of the bucket, or buckets that you
                                    would like to rebuild the search index for.
                                    If this is not sent along, all buckets will
                                    be rebuilt.  If multiple buckets are provided
                                    they should be comma separated.
                                    Example: -b "bucket1, bucket2, etc.."

        -c --chunk-size chunk-size  How many artifacts (per bucket) should be
                                    processed at once.
                                    [default: 20]

        -v --verbose                If set, the log level will be set to DEBUG.

    Arguments:
        <config-path>               Path to the yaml configuration file.
"""

args = docopt.docopt(doc)
log_level = logging.INFO

if args["--verbose"]:
    log_level = logging.DEBUG

logging.basicConfig(stream=sys.stdout, level=log_level)
logger = logging.getLogger()

config = {
    "logLevel": log_level,
    "chunkSize": args["--chunk-size"]
}

configure.app_config(config, args["<config-path>"])

bucket_string = args.get("--bucket")
bucket_list = []  # heh

if bucket_string:
    bucket_list = bucket_string.split(",")
    bucket_list = [val.strip() for val in bucket_list]

container = Container(config, logger)
container.runner.run(bucket_list)
