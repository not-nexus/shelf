from tests.unit_test_base import UnitTestBase
import tests.metadata_utils as utils
from tests.search.test_wrapper import TestWrapper as SearchTestWrapper


class UpdateManagerTest(UnitTestBase):
    def setUp(self):
        self.test_wrapper = SearchTestWrapper()
        self.update_manager = self.test_wrapper.search_container.update_manager
        self.test_wrapper.setup_metadata("test_key")

    def tearDown(self):
        self.test_wrapper.teardown_metadata("test_key")
        self.test_wrapper.teardown_metadata("test")

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
        first = self.update_manager.get_metadata("test_key").to_dict()
        second = self.update_manager.get_metadata("test").to_dict()
        expect_first = data["test_key"].values()
        expect_second = data["test"].values()
        self.assertEqual(first["items"], expect_first)
        self.assertEqual(second["items"], expect_second)

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
