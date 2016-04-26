from tests.functional_test_base import FunctionalTestBase
from pyshelf.bulk_update.utils import run_clean
from pyshelf.resource_identity import ResourceIdentity
import tests.metadata_utils as meta_utils
import os


class CleanerTest(FunctionalTestBase):
    def execute(self, log_dir=None, verbose=False):
        path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../data/functional_test_config.yaml")
        args = {
            "<config-path>": path,
            "--verbose": verbose,
            "--log-directory": log_dir
        }
        run_clean(args)

    def add_stale_docs(self, path_list):
        resource_list = []

        for path in path_list:
            resource_id = ResourceIdentity(path)
            data = meta_utils.get_meta(resource_id.artifact_name, resource_id.resource_path)
            self.search_wrapper.add_metadata(resource_id.search, data)
            resource_list.append(resource_id.search)

        self.search_wrapper.refresh_index()

        return resource_list

    def test_run_clean(self):
        path_list = [
            "/old/artifact/old",
            "/reallyold/artifact/ancient"
        ]
        resource_list = self.add_stale_docs(path_list)
        log_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../data/logging-dir")
        self.execute(log_dir=log_dir, verbose=True)

        actual = []
        for resource in resource_list:
            actual.append(self.search_wrapper.get_metadata(resource))

        self.assertEquals(actual, [None, None])
        log_file = os.path.join(log_dir, "clean-search-index.log")
        self.assertTrue(os.path.exists(log_file))
        os.remove(log_file)
