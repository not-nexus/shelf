#!/usr/bin/env python
import docopt
from pyshelf.bulk_update.utils import run_clean

doc = """Usage: ./clean-search-index [options] <config-path>

    Options:
        -v --verbose                If set, the log level will be set to DEBUG.

    Arguments:
        <config-path>               Path to the yaml configuration file.
"""

args = docopt.docopt(doc)
run_clean(args)
