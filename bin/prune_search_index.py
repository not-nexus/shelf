#!/usr/bin/env python
import docopt
from shelf.bulk_update.utils import prune

doc = """Usage: ./prune_search_index [options] <config-path>

    Options:
        -b --bucket bucket          The name of the bucket, or buckets that you
                                    would like to rebuild the search index for.
                                    If this is not sent along, all buckets will
                                    be rebuilt.  If multiple buckets are provided
                                    they should be comma separated.
                                    Example: -b "bucket1, bucket2, etc.."

        -v --verbose                If set, the log level will be set to DEBUG.

    Arguments:
        <config-path>               Path to the yaml configuration file.
"""

args = docopt.docopt(doc)
prune(args)
