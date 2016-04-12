import pyproctor
import logging
import sys


class TestBase(pyproctor.TestBase):
    @classmethod
    def setUpClass(cls):
        """
            This exists to make sure that no matter what, tests
            will log on stdout.  Every call to basicConfig after
            this point will be a no-op
        """
        logging.basicConfig(
            stream=sys.stdout
        )
