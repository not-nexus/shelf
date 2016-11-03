from shelf.metadata.bucket_container import BucketContainer
from shelf.metadata.yaml_codec import YamlCodec
from shelf.cloud.factory import Factory as CloudFactory
from shelf.search.container import Container as SearchContainer
from shelf.metadata.mapper import Mapper
from shelf.bucket_update.search_updater import SearchUpdater
from shelf.resource_identity_factory import ResourceIdentityFactory
from shelf.artifact_path_builder import ArtifactPathBuilder
from shelf.path_converter import PathConverter


class Container(object):
    def __init__(self, config, logger):
        """
            Args:
                config(schemas/search-bucket-update-config.json)
                logger(logging.Logger)
        """
        self.config = config
        self.logger = logger

        self._cloud_factory = None
        self._mapper = None
        self._codec = None
        self._search_container = None
        self._search_updater = None
        self._resource_identity_factory = None
        self._bucket_container = None

    @property
    def bucket_container(self):
        """
            Returns:
                shelf.metadata.bucket_container.BucketContainer
        """
        if not self._bucket_container:
            self._bucket_container = BucketContainer(
                self.config["referenceName"],
                self.codec,
                self.mapper,
                self.cloud_factory
            )

        return self._bucket_container

    @property
    def cloud_factory(self):
        """
            Returns:
                shelf.cloud.factory.Factory
        """
        if not self._cloud_factory:
            # TODO: This kind of sucks.  I shouldn't have to
            # recreate a different config format in order  to
            # use the cloud factory.
            config = {
                "buckets": [
                    self.config
                ]
            }
            self._cloud_factory = CloudFactory(config, self.logger)

        return self._cloud_factory

    @property
    def codec(self):
        """
            Returns:
                shelf.metadata.yaml_codec.YamlCodec
        """
        if not self._codec:
            self._codec = YamlCodec()

        return self._codec

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
    def search_container(self):
        """
            Returns:
                shelf.search.container.Container
        """
        if not self._search_container:
            self._search_container = SearchContainer(
                self.logger,
                self.config["elasticsearch"]
            )

        return self._search_container

    @property
    def search_updater(self):
        """
            Returns:
                shelf.bucket_update.search_updater
        """
        if not self._search_updater:
            self._search_updater = SearchUpdater(self)

        return self._search_updater

    @property
    def resource_identity_factory(self):
        """
            Returns:
                shelf.resource_identity_factory.ResourceIdentityFactory
        """
        if not self._resource_identity_factory:
            builder = ArtifactPathBuilder(self.config["referenceName"])
            path_converter = PathConverter(builder)
            self._resource_identity_factory = ResourceIdentityFactory(path_converter)

        return self._resource_identity_factory
