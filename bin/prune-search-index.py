#!/usr/bin/env python
import docopt
from pyshelf.bulk_update.utils import run_search_prune

doc = """Usage: ./prune-search-index [options] <config-path>

    Options:
        -v --verbose                If set, the log level will be set to DEBUG.

        -d=DIR --log-direcory=DIR   Directory to output logs to. Outputs to stdout
                                    if directory not given.

    Arguments:
        <config-path>               Path to the yaml configuration file.
"""

args = docopt.docopt(doc)
run_search_prune(args)
