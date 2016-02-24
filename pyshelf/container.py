from uuid import uuid4
from pyshelf.permissions_validator import PermissionsValidator
from pyshelf.cloud.factory import Factory


class Container(object):
    def __init__(self, app, request=None):
        """
            param flask.Flask app
            param flask.Request request
        """
        self.app = app
        self.request = request
        self.request_id = uuid4().hex

        # services
        self._permissions_validator = None
        self._cloud_factory = None
        self._artifact_list_manager = None

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

    def create_master_bucket_storage(self):
        bucket_name = self.app.config["bucketName"]
        return self.cloud_factory.create_storage(bucket_name)
