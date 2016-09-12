import pyproctor
from mock import Mock
from pyshelf.container import Container


class ContainerTest(pyproctor.TestBase):
    def test_container_no_bucket_name(self):
        """
            This is an unlikely scenario because of our
            config validation but if the container is used directly
            it could happen so I figure I might as well test it.
        """
        with self.assertRaises(Exception):
            container = Container(Mock())
            container.metadata
