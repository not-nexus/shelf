from pyshelf.metadata.cloud_portal import CloudPortal
from pyshelf.metadata.initializer import Initializer


class BucketContainer(object):
    """
        The point of this class is to add things that are specific
        to a bucket and NOT specific to a particular artifact or
        resource
    """
    def __init__(self, bucket_name, yaml_codec, mapper, cloud_factory):
        """
            Args:
                bucket_name(basestring)
                yaml_codec(pyshelf.metadata.yaml_codec.YamlCodec)
                mapper(pyshelf.metadata.mapper.Mapper)
                cloud_factory(pyshelf.cloud.factory.Factory)
        """
        self.yaml_codec = yaml_codec
        self.mapper = mapper
        self.cloud_factory = cloud_factory
        self.bucket_name = bucket_name

        self._cloud_portal = None
        self._initializer = None

    @property
    def cloud_portal(self):
        """
            Returns:
                pyshelf.metadata.cloud_portal.CloudPortal
        """
        if not self._cloud_portal:
            self._cloud_portal = CloudPortal(self)

        return self._cloud_portal

    @property
    def initializer(self):
        """
            Returns:
                pyshelf.metadata.initializer.Initializer
        """
        if not self._initializer:
            self._initializer = Initializer(self)

        return self._initializer

    def create_cloud_storage(self):
        """
            Returns:
                pyshelf.cloud.storage.Storage
        """
        return self.cloud_factory.create_storage(self.bucket_name)
