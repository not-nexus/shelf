from tests.unit_test_base import UnitTestBase
import tests.metadata_utils as utils
from tests.search.test_wrapper import TestWrapper as SearchTestWrapper
from pyshelf.search.update_manager import UpdateManager
from pyshelf.search.manager import Manager as SearchManager
from pyshelf.search.metadata import Metadata
from pyshelf.search.type import Type as SearchType


class UpdateManagerTest(UnitTestBase):
    def setUp(self):
        self.test_wrapper = SearchTestWrapper()
        self.update_manager = self.test_wrapper.update_manager
        self.test_wrapper.setup_metadata("test_key")

    def tearDown(self):
        self.test_wrapper.teardown_metadata("test_key")

    def test_metadata_update(self):
        self.update_manager.update("test_key", utils.get_meta())
        metadata = self.update_manager.get_metadata("test_key")
        self.assertEqual(metadata.to_dict(), {"items": utils.get_meta_elastic()})

    def test_metadata_update_item(self):
        self.update_manager.update_item("test_key", utils.get_meta_item())
        metadata = self.update_manager.get_metadata("test_key").to_dict()
        got_it = False
        for item in metadata["items"]:
            if item["name"] == "tag2":
                self.assertEqual(item, utils.get_meta_item())
                got_it = True
        self.assertTrue(got_it)
