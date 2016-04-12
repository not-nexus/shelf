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
        # AGI-731
        # See jira for more information
        #
        # https://github.com/gabrielfalcao/HTTPretty/issues/280
        #
        # logging.basicConfig(
        #     stream=sys.stdout
        # )
