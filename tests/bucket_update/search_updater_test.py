from tests.bucket_update.test_base import TestBase
from mock import Mock


class SearchUpdaterTest(TestBase):
    def test_all(self):
        """
            Supposed to be a generic test that will check that
            metadata is created, updated and deleted in the
            search layer.
        """

        # metadata only in the cloud should be added to search
        add_builder = self.create_metadata_builder() \
            .property("test", "test") \
            .resource_url("/test-refname/artifact/kyle-test/add")
        self.add_cloud(add_builder)
        self.add_cloud_artifact(add_builder)

        # metadata only in the search layer should be deleted.
        delete_builder = self.create_metadata_builder() \
            .resource_url("/test-refname/artifact/lyle-test/delete-me")

        self.add_search(delete_builder)

        # metadata in both should get updated
        update_search_builder = self.create_metadata_builder() \
            .property("lol", "not-lol") \
            .resource_url("/test-refname/artifact/jyle-test/needs-update")

        update_cloud_builder = update_search_builder \
            .copy() \
            .property("lol", "is-lol")

        self.add_search(update_search_builder)
        self.add_cloud(update_cloud_builder)
        self.add_cloud_artifact(update_cloud_builder)

        # Important because if these docs were JUST added
        # to elasticsearch they will not end up being found
        # when doing the bulk update.  In practice this shouldn't
        # happen unless in very quick succession we add metadata
        # then manually delete it in S3 and then run bucket-update
        # really really quick.
        self.search_wrapper.refresh_index()
        
        # Running actual code
        runner = self.container.search_updater
        runner.run()

        # These two artifacts should have identity metadata in both
        # search and cloud
        self.assert_metadata_matches(add_builder.identity.resource_url, "test")
        self.assert_metadata_matches(update_search_builder.identity.resource_url, "test")

        # This should have been deleted
        should_be_deleted = self.search_wrapper.get_metadata(delete_builder.identity.search)
        self.assertEqual(None, should_be_deleted)

    def test_no_artifacts(self):
        bucket_name = "bucket-that-doesnt-have-artifacts"
        self.boto_connection.create_bucket(bucket_name)
        self.container.config["name"] = bucket_name
        logger = self.container.logger
        logger.info = Mock()
        updater = self.container.search_updater
        updater.run()

    def run_chunk(self, chunk_size, path_list, expected_list):
        search_updater = self.container.search_updater
        search_updater.chunk_size = chunk_size
        actual_list = []
        for chunk in search_updater._chunk(path_list):
            actual_list.append(chunk)

        self.assertEqual(expected_list, actual_list)

    def test_less_than_chunk(self):
        path_list = [
            "abc123",
            "abc124",
        ]

        expected_list = [
            [
                "abc123",
                "abc124"
            ]
        ]

        self.run_chunk(3, path_list, expected_list)

    def test_more_than_chunk(self):
        path_list = [1, 2, 3, 4]

        expected_list = [
            [1, 2, 3],
            [4]
        ]

        self.run_chunk(3, path_list, expected_list)

    def test_exactly_chunk(self):
        path_list = [1, 2, 3, 4, 5, 6]

        expected_list = [
            [1, 2, 3],
            [4, 5, 6]
        ]

        self.run_chunk(3, path_list, expected_list)
