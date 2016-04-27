#!/usr/bin/env python
import docopt
from pyshelf.bulk_update.utils import run_search_prune

doc = """Usage: ./prune-search-index [options] <config-path>

    Options:
        -v --verbose                If set, the log level will be set to DEBUG.

    Arguments:
        <config-path>               Path to the yaml configuration file.
"""

args = docopt.docopt(doc)
run_search_prune(args)
