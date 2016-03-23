from uuid import uuid4
from pyshelf.permissions_validator import PermissionsValidator
from pyshelf.cloud.factory import Factory
from pyshelf.artifact_list_manager import ArtifactListManager
from pyshelf.link_mapper import LinkMapper
from pyshelf.context import Context


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
        self._link_mapper = None
        self._context = None

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

    def create_master_bucket_storage(self):
        return self.cloud_factory.create_storage(self.bucket_name)

    @property
    def link_mapper(self):
        if not self._link_mapper:
            self._link_mapper = LinkMapper(self.bucket_name)

        return self._link_mapper

    @property
    def context(self):
        if not self._context:
            self._context = Context()

        return self._context
