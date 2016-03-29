from uuid import uuid4
from pyshelf.permissions_validator import PermissionsValidator
from pyshelf.cloud.factory import Factory
from pyshelf.artifact_list_manager import ArtifactListManager
from pyshelf.search.container import Container as SearchContainer
from pyshelf.search_portal import SearchPortal
from pyshelf.link_mapper import LinkMapper
from pyshelf.context import Context
from pyshelf.context_response_mapper import ContextResponseMapper
from pyshelf.link_manager import LinkManager
from pyshelf.artifact_path_builder import ArtifactPathBuilder
from pyshelf.search_parser import SearchParser
from pyshelf.resource_identity import ResourceIdentity
from pyshelf.metadata.container import Container as MetadataContainer


class Container(object):
    def __init__(self, app, request=None):
        """
            param flask.Flask app
            param flask.Request request
        """
        self.app = app
        self.request = request
        self.request_id = uuid4().hex
        self.bucket_name = None

        # services
        self._permissions_validator = None
        self._cloud_factory = None
        self._artifact_list_manager = None
        self._search = None
        self._link_mapper = None
        self._context = None
        self._context_response_mapper = None
        self._link_manager = None
        self._artifact_path_builder = None
        self._search_portal = None
        self._search_parser = None
        self._resource_identity = None
        self._metadata = None

    @property
    def logger(self):
        return self.app.logger

    @property
    def permissions_validator(self):
        if not self._permissions_validator:
            self._permissions_validator = PermissionsValidator(self)

        return self._permissions_validator

    @property
    def cloud_factory(self):
        if not self._cloud_factory:
            self._cloud_factory = Factory(self.app.config, self.app.logger)

        return self._cloud_factory

    @property
    def artifact_list_manager(self):
        if not self._artifact_list_manager:
            self._artifact_list_manager = ArtifactListManager(self)

        return self._artifact_list_manager

    @property
    def search(self):
        if not self._search:
            self._search = SearchContainer(self.app.logger, self.app.config.get("elasticSearchHost"))

        return self._search

    def create_bucket_storage(self):
        return self.cloud_factory.create_storage(self.bucket_name)

    @property
    def link_mapper(self):
        if not self._link_mapper:
            self._link_mapper = LinkMapper(self.artifact_path_builder)

        return self._link_mapper

    @property
    def context(self):
        if not self._context:
            self._context = Context()

        return self._context

    @property
    def context_response_mapper(self):
        if not self._context_response_mapper:
            self._context_response_mapper = ContextResponseMapper(self.link_mapper, self._context)

        return self._context_response_mapper

    @property
    def link_manager(self):
        if not self._link_manager:
            self._link_manager = LinkManager(self)

        return self._link_manager

    @property
    def artifact_path_builder(self):
        if not self._artifact_path_builder:
            self._artifact_path_builder = ArtifactPathBuilder(self.bucket_name)

        return self._artifact_path_builder

    @property
    def search_portal(self):
        if not self._search_portal:
            self._search_portal = SearchPortal(self)

        return self._search_portal

    @property
    def search_parser(self):
        if not self._search_parser:
            self._search_parser = SearchParser()

        return self._search_parser

    @property
    def resource_identity(self):
        if not self._resource_identity:
            self._resource_identity = ResourceIdentity(self.request.path)

        return self._resource_identity

    @property
    def metadata(self):
        if not self._metadata:
            if not self.bucket_name:
                raise Exception("bucket_name must exist to create pyshelf.metadata.container.Container")

            self._metadata = MetadataContainer(
                self.bucket_name,
                self.cloud_factory,
                self.resource_identity,
                self.search.update_manager
            )

        return self._metadata
