from tests.unit_test_base import UnitTestBase
import tests.metadata_utils as utils
from tests.search.test_wrapper import TestWrapper as SearchTestWrapper
from pyshelf.search.metadata import Metadata


class UpdateManagerTest(UnitTestBase):
    def setUp(self):
        super(UpdateManagerTest, self).setUp()
        self.test_wrapper = SearchTestWrapper(self.search_container)
        self.update_manager = self.search_container.update_manager
        data = [utils.get_meta("test_key"), utils.get_meta("delete"), utils.get_meta("old")]
        self.test_wrapper.setup_metadata(data)

    def tearDown(self):
        self.test_wrapper.teardown_metadata()

    def test_remove_old_docs(self):
        key_list = ["test_key", "test"]
        self.update_manager.remove_unlisted_documents(key_list)
        self.assertEqual(self.test_wrapper.get_metadata("delete"), None)
        self.assertEqual(self.test_wrapper.get_metadata("old"), None)
        self.assertEqual(self.test_wrapper.get_metadata("test_key").to_dict()["items"],
                utils.get_meta_elastic("test_key"))

    def test_bulk_update(self):
        data = {
            "test_key": {
                "name": {
                    "name": "name",
                    "value": "value",
                    "immutable": True
                }
            },
            "test": {
                "name": {
                    "name": "name",
                    "value": "value",
                    "immutable": False
                },
                "die": {
                    "name": "die",
                    "value": "no one reads this anyway",
                    "immutable": True
                }
            }
        }
        self.update_manager.bulk_update(data)
        first = self.update_manager._get_metadata("test_key").to_dict()
        second = self.update_manager._get_metadata("test").to_dict()
        expect_first = data["test_key"].values()
        expect_second = data["test"].values()
        self.assertEqual(first["items"], expect_first)
        self.assertEqual(second["items"], expect_second)

    def test_metadata_update(self):
        self.update_manager.update("test_key", utils.get_meta())
        metadata = self.update_manager._get_metadata("test_key")
        self.assertEqual(metadata.to_dict(), {"items": utils.get_meta_elastic()})
