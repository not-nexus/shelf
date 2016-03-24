from uuid import uuid4
from pyshelf.permissions_validator import PermissionsValidator
from pyshelf.cloud.factory import Factory
from pyshelf.artifact_list_manager import ArtifactListManager
from pyshelf.search.services import Services as SearchServices
from pyshelf.search_portal import SearchPortal
from pyshelf.link_mapper import LinkMapper
from pyshelf.context import Context
from pyshelf.context_response_mapper import ContextResponseMapper
from pyshelf.link_manager import LinkManager
from pyshelf.artifact_path_builder import ArtifactPathBuilder


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
            self._search = SearchServices(self)

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
