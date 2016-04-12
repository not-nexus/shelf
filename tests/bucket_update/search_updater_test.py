from boto.s3.key import Key
from pyshelf.bucket_update.container import Container
from tests.functional_test_base import FunctionalTestBase
from tests.metadata.factory import Factory
import logging
import sys


class SearchUpdaterTest(FunctionalTestBase):
    def setUp(self):
        super(SearchUpdaterTest, self).setUp()
        self.fake_config = {
            "name": "test",
            "accessKey": "ABC123",
            "secretKey": "321CBA",
            "elasticSearchConnectionString": FunctionalTestBase.ELASTICSEARCH_CONNECTION_STRING,
            "logLevel": logging.INFO,
            "chunkSize": 10
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

    def test_all(self):
        """
            Supposed to be a generic test that will check that
            metadata is created, updated and deleted in the
            search layer.
        """

        # metadata only in the cloud should be added to search
        add_builder = self.create_metadata_builder() \
            .property("test", "test") \
            .resource_url("/test/artifact/kyle-test/add")
        self.add_cloud(add_builder)
        self.add_cloud_artifact(add_builder)

        # metadata only in the search layer should be deleted.
        delete_builder = self.create_metadata_builder() \
            .resource_url("/test/artifact/lyle-test/delete-me")

        self.add_search(delete_builder)

        # metadata in both should get updated
        update_search_builder = self.create_metadata_builder() \
            .property("lol", "not-lol") \
            .resource_url("/test/artifact/jyle-test/needs-update")

        update_cloud_builder = update_search_builder \
            .copy() \
            .property("lol", "is-lol")

        self.add_search(update_search_builder)
        self.add_cloud(update_cloud_builder)
        self.add_cloud_artifact(update_cloud_builder)

        runner = self.container.search_updater
        runner.run()

        # These two artifacts should have identity metadata in both
        # search and cloud
        self.assert_metadata_matches(add_builder.identity.resource_url)
        self.assert_metadata_matches(update_search_builder.identity.resource_url)

        # This should have been deleted
        should_be_deleted = self.search_wrapper.get_metadata(delete_builder.identity.search)
        self.assertEqual(None, should_be_deleted)
