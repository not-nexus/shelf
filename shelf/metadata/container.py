from shelf.metadata.mapper import Mapper
from shelf.metadata.manager import Manager
from shelf.metadata.yaml_codec import YamlCodec
from shelf.metadata.bucket_container import BucketContainer
from shelf.metadata.wrapper import Wrapper


class Container(object):
    def __init__(self, bucket_name, cloud_factory, resource_identity, update_manager):
        self.bucket_name = bucket_name
        self.cloud_factory = cloud_factory
        self.resource_identity = resource_identity
        self.update_manager = update_manager
        self._mapper = None
        self._manager = None
        self._yaml_codec = None
        self._bucket_container = None

    def create_wrapper(self, metadata):
        """
            Returns:
                shelf.metadata.wrapper.Wrapper
        """
        return Wrapper(metadata)

    @property
    def mapper(self):
        """
            Returns:
                shelf.metadata.mapper.Mapper
        """
        if not self._mapper:
            self._mapper = Mapper()

        return self._mapper

    @property
    def manager(self):
        """
            Returns:
                shelf.metadata.manager.Manager
        """
        if not self._manager:
            self._manager = Manager(self)

        return self._manager

    @property
    def yaml_codec(self):
        """
            Returns:
                shelf.metadata.yaml_codec.YamlCodec
        """
        if not self._yaml_codec:
            self._yaml_codec = YamlCodec()

        return self._yaml_codec

    @property
    def bucket_container(self):
        """
            Returns:
                shelf.metadata.bucket_container.BucketContainer
        """
        if not self._bucket_container:
            self._bucket_container = BucketContainer(
                self.bucket_name,
                self.yaml_codec,
                self.mapper,
                self.cloud_factory
            )

        return self._bucket_container
