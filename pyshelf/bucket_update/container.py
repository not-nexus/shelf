from pyshelf.metadata.bucket_container import BucketContainer
from pyshelf.metadata.yaml_codec import YamlCodec
from pyshelf.cloud.factory import Factory as CloudFactory
from pyshelf.search.container import Container as SearchContainer
from pyshelf.metadata.mapper import Mapper
from pyshelf.bucket_update.search_updater import SearchUpdater
from pyshelf.resource_identity_factory import ResourceIdentityFactory
from pyshelf.artifact_path_builder import ArtifactPathBuilder


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
            Args:
                bucket_name(basestring)

            Returns:
                pyshelf.metadata.bucket_container.BucketContainer
        """
        if not self._bucket_container:
            self._bucket_container = BucketContainer(
                self.config["name"],
                self.codec,
                self.mapper,
                self.cloud_factory
            )

        return self._bucket_container

    @property
    def cloud_factory(self):
        """
            Returns:
                pyshelf.cloud.factory.Factory
        """
        if not self._cloud_factory:
            # TODO: This kind of sucks.  I shouldn't have to
            # recreate a different config format in order  to
            # use the cloud factory.
            config = {
                "buckets": {
                    self.config["name"]: self.config
                }
            }
            self._cloud_factory = CloudFactory(config, self.logger)

        return self._cloud_factory

    @property
    def codec(self):
        """
            Returns:
                pyshelf.metadata.yaml_codec.YamlCodec
        """
        if not self._codec:
            self._codec = YamlCodec()

        return self._codec

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
    def search_container(self):
        if not self._search_container:
            self._search_container = SearchContainer(
                self.logger,
                self.config["elasticSearchConnectionString"]
            )

        return self._search_container

    @property
    def search_updater(self):
        """
            Returns:
                pyshelf.bucket_update.search_updater
        """
        if not self._search_updater:
            self._search_updater = SearchUpdater(self)

        return self._search_updater

    @property
    def resource_identity_factory(self):
        if not self._resource_identity_factory:
            builder = ArtifactPathBuilder(self.config["name"])
            self._resource_identity_factory = ResourceIdentityFactory(builder)

        return self._resource_identity_factory
