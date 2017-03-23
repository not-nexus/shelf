from shelf import utils
from shelf.artifact_manager import ArtifactManager
from shelf.artifact_path_builder import ArtifactPathBuilder
from shelf.cloud.factory import Factory
from shelf.context import Context
from shelf.context_response_mapper import ContextResponseMapper
from shelf.hook.container import Container as HookContainer
from shelf.link_manager import LinkManager
from shelf.link_mapper import LinkMapper
from shelf.list_shelves_manager import ListShelvesManager
from shelf.metadata.container import Container as MetadataContainer
from shelf.null_handler import NullHandler
from shelf.path_converter import PathConverter
from shelf.permissions_loader import PermissionsLoader
from shelf.permissions_validator import PermissionsValidator
from shelf.resource_identity_factory import ResourceIdentityFactory
from shelf.schema_validator import SchemaValidator
from shelf.search.container import Container as SearchContainer
from shelf.search_parser import SearchParser
from shelf.search_portal import SearchPortal
from uuid import uuid4
import logging


class Container(object):
    def __init__(self, app, request=None):
        """
            Args:
                app(flask.Flask)
                request(flask.Request)
        """
        self.app = app
        self.request = request
        self.request_id = uuid4().hex
        self.bucket_name = None

        # services
        self._permissions_validator = None
        self._permissions_loader = None
        self._cloud_factory = None
        self._artifact_manager = None
        self._search = None
        self._link_mapper = None
        self._context = None
        self._context_response_mapper = None
        self._link_manager = None
        self._artifact_path_builder = None
        self._search_portal = None
        self._search_parser = None
        self._resource_identity = None
        self._resource_identity_factory = None
        self._metadata = None
        self._schema_validator = None
        self._path_converter = None
        self._silent_logger = None
        self._silent_cloud_factory = None
        self._hook = None
        self._hook_manager = None
        self._list_shelves_manager = None

    @property
    def logger(self):
        return self.app.logger

    @property
    def silent_logger(self):
        """
            A logger that will not log anything.

            Returns:
                logging.Logger
        """
        if not self._silent_logger:
            self._silent_logger = logging.Logger("SilentLogger")
            self._silent_logger.addHandler(NullHandler())

        return self._silent_logger

    @property
    def list_shelves_manager(self):
        if not self._list_shelves_manager:
            shelf_list = [b["referenceName"] for b in self.app.config.get("buckets")]
            self._list_shelves_manager = ListShelvesManager(shelf_list, self.permissions_loader)

        return self._list_shelves_manager

    @property
    def permissions_loader(self):
        if not self._permissions_loader:
            self._permissions_loader = PermissionsLoader(self.logger, self.silent_cloud_factory)

        return self._permissions_loader

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
    def silent_cloud_factory(self):
        """
            A factory whose objects it creates will not
            log anything.

            Returns:
                shelf.cloud.factory.Factory
        """
        if not self._silent_cloud_factory:
            self._silent_cloud_factory = Factory(self.app.config, self.silent_logger)

        return self._silent_cloud_factory

    @property
    def artifact_manager(self):
        if not self._artifact_manager:
            self._artifact_manager = ArtifactManager(self)

        return self._artifact_manager

    @property
    def search(self):
        if not self._search:
            self._search = SearchContainer(self.app.logger, self.app.config.get("elasticsearch"))

        return self._search

    def create_bucket_storage(self):
        return self.cloud_factory.create_storage(self.bucket_name)

    def create_silent_bucket_storage(self):
        """
            Just like a normal Storage object except that the logger will
            not log anything.

            Returns:
                shelf.cloud.storage.Storage
        """
        return self.silent_cloud_factory.create_storage(self.bucket_name)

    @property
    def link_mapper(self):
        if not self._link_mapper:
            self._link_mapper = LinkMapper()

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
            self._resource_identity = self.resource_identity_factory.from_resource_url(self.request.path)

        return self._resource_identity

    @property
    def schema_validator(self):
        if not self._schema_validator:
            self._schema_validator = SchemaValidator(self.logger)

        return self._schema_validator

    @property
    def resource_identity_factory(self):
        if not self._resource_identity_factory:
            self._resource_identity_factory = ResourceIdentityFactory(self.path_converter)

        return self._resource_identity_factory

    @property
    def metadata(self):
        if not self._metadata:
            if not self.bucket_name:
                raise Exception("bucket_name must exist to create shelf.metadata.container.Container")

            self._metadata = MetadataContainer(
                self.bucket_name,
                self.cloud_factory,
                self.resource_identity,
                self.search.update_manager,
                self.hook_manager
            )

        return self._metadata

    @property
    def path_converter(self):
        if not self._path_converter:
            self._path_converter = PathConverter(self.artifact_path_builder)

        return self._path_converter

    @property
    def hook(self):
        """
            Returns:
                shelf.hook.container.Container
        """
        if not self._hook:
            self._hook = HookContainer(self.logger)

        return self._hook

    @property
    def hook_manager(self):
        """
            Returns:
                shelf.hook.manager.Manager
        """
        if not self._hook_manager:
            hook_command = self.app.config.get("hookCommand")

            if hook_command:
                host = utils.get_host_from_uri(self.request.url)
                self._hook_manager = self.hook.create_manager(host, hook_command)
            else:
                self._hook_manager = self.hook.create_null_manager()

        return self._hook_manager
