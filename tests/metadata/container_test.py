import pyproctor
from tests.metadata.factory import Factory
from mock import Mock


class ContainerTest(pyproctor.TestBase):
    def test_container_no_bucket_name(self):
        """
            This is an unlikely scenario because of out 
            config validation but if the container is used directly
            it could happen so I figure I might as well test it.
        """
        factory = Factory(Mock())

        with self.assertRaises(Exception):
            container = factory.create_fake_container(None)
            container.metadata
