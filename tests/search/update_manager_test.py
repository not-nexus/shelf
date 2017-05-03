from tests.unit_test_base import UnitTestBase
import tests.metadata_utils as utils
from tests.search.test_wrapper import TestWrapper as SearchTestWrapper


class UpdateManagerTest(UnitTestBase):
    def setUp(self):
        super(UpdateManagerTest, self).setUp()
        self.test_wrapper = SearchTestWrapper(self.search_container)
        self.update_manager = self.search_container.update_manager
        data = [
            utils.get_meta("test_key"),
            utils.get_meta("delete"),
            utils.get_meta("old"),
            # In another bucket
            utils.get_meta("other", "/other/artifact/other"),
            utils.get_meta("ricki", "/ricki/artifact/ticki/tabi")
        ]
        self.test_wrapper.setup_metadata(data)

    def tearDown(self):
        self.test_wrapper.teardown_metadata()

    def test_remove_all_old_docs(self):
        key_list = ["test_key"]
        deleted = self.update_manager.remove_unlisted_documents(key_list)
        self.assertEqual(4, deleted)
        self.assertEqual(None, self.test_wrapper.get_metadata("delete"))
        self.assertEqual(None, self.test_wrapper.get_metadata("old"))
        self.assertEqual(None, self.test_wrapper.get_metadata("other"))
        self.assertEqual(None, self.test_wrapper.get_metadata("ricki"))

    def test_remove_old_docs_per_bucket(self):
        key_list = ["test_key"]
        deleted = self.update_manager.remove_unlisted_documents_per_bucket(key_list, "test")
        self.assertEqual(2, deleted)
        self.assertEqual(None, self.test_wrapper.get_metadata("delete"))
        self.assertEqual(None, self.test_wrapper.get_metadata("old"))

    def test_remove_documents_wildcard(self):
        val_list = [
            "/test/artifact/*",
            "/ricki/artifact/*"
        ]
        deleted = self.update_manager.remove_unlisted_documents_wildcard("artifactPath", val_list)
        self.assertEqual(1, deleted)
        self.assertEqual(None, self.test_wrapper.get_metadata("other"))

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
        self.assertEqual(first["property_list"], expect_first)
        self.assertEqual(second["property_list"], expect_second)

    def test_metadata_update(self):
        self.update_manager.update("test_key", utils.get_meta())
        metadata = self.update_manager._get_metadata("test_key")
        self.assertEqual(metadata.to_dict(), {"property_list": utils.get_meta_elastic()})
