from pyshelf.metadata.mapper import Mapper
from pyshelf.metadata.wrapper import Wrapper
from pyshelf.metadata.manager import Manager
from pyshelf.metadata.yaml_codec import YamlCodec
from pyshelf.metadata.cloud_portal import CloudPortal
from pyshelf.metadata.initializer import Initializer
from pyshelf.metadata.bucket_container import BucketContainer


class Container(object):
    def __init__(self, bucket_name, cloud_factory, resource_identity):
        self.bucket_name = bucket_name
        self.cloud_factory = cloud_factory
        self.resource_identity = resource_identity
        self._mapper = None
        self._manager = None
        self._yaml_codec = None
        self._bucket_container = None

    def create_wrapper(self, metadata):
        """
            Returns:
                pyshelf.metadata.wrapper.Wrapper
        """
        return Wrapper(metadata)

    @property
    def mapper(self):
        """
            Returns:
                pyshelf.metadata.mapper.Mapper
        """
        if not self._mapper:
            self._mapper = Mapper()

        return self._mapper

    @property
    def manager(self):
        """
            Returns:
                pyshelf.metadata.manager.Manager
        """
        if not self._manager:
            self._manager = Manager(self)

        return self._manager

    @property
    def yaml_codec(self):
        """
            Returns:
                pyshelf.metadata.yaml_codec.YamlCodec
        """
        if not self._yaml_codec:
            self._yaml_codec = YamlCodec()

        return self._yaml_codec

    @property
    def bucket_container(self):
        """
            Returns:
                pyshelf.metadata.bucket_container.BucketContainer
        """
        if not self._bucket_container:
            self._bucket_container = BucketContainer(
                self.bucket_name,
                self.yaml_codec,
                self.mapper,
                self.cloud_factory
            )

        return self._bucket_container
