from pyshelf.metadata.mapper import Mapper
from pyshelf.metadata.wrapper import Wrapper
from pyshelf.metadata.manager import Manager
from pyshelf.metadata.yaml_codec import YamlCodec


class Container(object):
    def __init__(self, bucket_name, cloud_factory, resource_identity):
        self.bucket_name = bucket_name
        self.cloud_factory = cloud_factory
        self.resource_identity = resource_identity
        self._mapper = None
        self._manager = None
        self._yaml_codec = None

    def create_cloud_storage(self):
        return self.cloud_factory.create_storage(self.bucket_name)

    def create_wrapper(self, metadata):
        return Wrapper(metadata)

    @property
    def mapper(self):
        if not self._mapper:
            self._mapper = Mapper()

        return self._mapper

    @property
    def manager(self):
        if not self._manager:
            self._manager = Manager(self)

        return self._manager

    @property
    def yaml_codec(self):
        if not self._yaml_codec:
            self._yaml_codec = YamlCodec()

        return self._yaml_codec
