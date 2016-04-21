from tests.functional_test_base import FunctionalTestBase
import logging
from boto.s3.key import Key
from pyshelf.bucket_update.container import Container
from tests.metadata.factory import Factory
import sys


class TestBase(FunctionalTestBase):
    def setUp(self):
        super(TestBase, self).setUp()
        self.fake_config = {
            "name": "test",
            "accessKey": "ABC123",
            "secretKey": "321CBA",
            "elasticsearch": FunctionalTestBase.CONFIG["elasticsearch"],
            "logLevel": logging.INFO,
            "chunkSize": 10,
            "referenceName": "test"
        }

        self.logger = self.create_logger()
        self.factory = Factory(self.logger)
        self.container = Container(self.fake_config, self.logger)
        self.cloud_portal = self.factory.create_cloud_portal(self.fake_config["name"])

    def create_logger(self):
        handler = logging.StreamHandler(stream=sys.stdout)
        logger = logging.Logger(self.fake_config["name"])
        logger.addHandler(handler)
        return logger

    def add_cloud_artifact(self, builder):
        key = Key(self.test_bucket, builder.identity.cloud)
        key.set_contents_from_string("test")

    def add_cloud(self, builder):
        self.cloud_portal.update(builder.identity.cloud_metadata, builder.data)

    def add_search(self, builder):
        self.search_wrapper.add_metadata(builder.identity.search, builder.data)

    def add_both(self, builder):
        self.add_cloud(builder)
        self.add_search(builder)
