from tests.functional_test_base import FunctionalTestBase
from shelf.bucket_update.utils import prune_search_index
from shelf.resource_identity import ResourceIdentity
import shelf.configure as configure
import tests.metadata_utils as meta_utils
import os


class PruneSearchIndexTest(FunctionalTestBase):
    def execute(self):
        bucket_names = []
        config = {}
        config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../data/functional_test_config.yaml")
        configure.app_config(config, config_path)

        for bucket_config in config.get("buckets"):
            # Append to a list so we can clean up the log files.
            bucket_names.append(bucket_config["name"])
            bucket_config.update({
                "elasticsearch": config["elasticsearch"],
                "logLevel": 20,  # logLevel is "info"
                "bulkUpdateLogDirectory": config["bulkUpdateLogDirectory"]
            })
            prune_search_index(bucket_config)

        return bucket_names

    def add_stale_docs(self, path_list):
        resource_list = []

        for path in path_list:
            resource_id = ResourceIdentity(path)
            data = meta_utils.get_meta(resource_id.artifact_name, resource_id.resource_path)
            self.search_wrapper.add_metadata(resource_id.search, data)
            resource_list.append(resource_id.search)

        self.search_wrapper.refresh_index()

        return resource_list

    def test_run_prune(self):
        path_list = [
            "/test/artifact/old",
            "/b2/artifact/ancient"
        ]

        # These artifacts are setup in moto in functional test.
        # Making sure only the appropriate documents are deleted.
        existing_list = [
            "/test/artifact/test",
            "/test/artifact/dir/dir2/dir3/nest-test"
        ]
        self.add_stale_docs(path_list)
        bucket_names = self.execute()
        self.search_wrapper.refresh_index()
        self.assert_docs(path_list, [])
        self.assert_docs(existing_list, existing_list)

        for bucket_name in bucket_names:
            log_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../data/logging-dir")
            log_file = os.path.join(log_dir, "{0}.log".format(bucket_name))
            self.assertTrue(os.path.exists(log_file))
            os.remove(log_file)

    def assert_docs(self, path_list, expected):
        actual = []

        for path in path_list:
            resource_id = ResourceIdentity(path)
            metadata = self.search_wrapper.get_metadata(resource_id.search)

            if metadata is not None:
                for prop in metadata.to_dict()["property_list"]:
                    if prop["name"] == "artifactPath":
                        actual.append(prop["value"])

        self.assertEquals(expected, actual)
