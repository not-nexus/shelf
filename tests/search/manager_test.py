from tests.unit_test_base import UnitTestBase
from tests.search.test_wrapper import TestWrapper as SearchTestWrapper
from pyshelf.search.type import Type as SearchType
import tests.metadata_utils as utils
import time


class ManagerTest(UnitTestBase):
    def setUp(self):
        self.test_wrapper = SearchTestWrapper()
        self.search_manager = self.test_wrapper.search_manager
        self.test_wrapper.setup_metadata()
        self.test_wrapper.setup_metadata("other", "/this/that/other", "1.1")
        self.test_wrapper.setup_metadata("thing", "/thing", "1.2")
        # temp fix
        time.sleep(1)

    def tearDown(self):
        self.test_wrapper.teardown_metadata("test")
        self.test_wrapper.teardown_metadata("other")
        self.test_wrapper.teardown_metadata("thing")

    def test_equality_search(self):
        results = self.search_manager.search({
            "artifactName": {
                "searchType": SearchType.MATCH,
                "value": "test"
            },
            "artifactPath": {
                "searchType": SearchType.WILDCARD,
                "value": "tes?"
            }
        })
        self.assertEqual(len(results), 1)
        self.assertEqual(results["test"], utils.get_meta_elastic())

    def test_tilde_search(self):
        results = self.search_manager.search({
            "version": {
                "searchType": SearchType.TILDE,
                "value": "1.1"
            }
        })
        self.assertEqual(len(results), 2)
        self.assertEqual(results["other"], utils.get_meta_elastic("other", "/this/that/other", "1.1"))
        self.assertEqual(results["thing"], utils.get_meta_elastic("thing", "/thing", "1.2"))

    def test_tilde_wildcard(self):
        results = self.search_manager.search({
            "version": {
                "searchType": SearchType.WILDCARD_TILDE,
                "value": "*.1"
            }
        })
        self.assertEqual(len(results), 2)
        self.assertEqual(results["other"], utils.get_meta_elastic("other", "/this/that/other", "1.1"))
        self.assertEqual(results["thing"], utils.get_meta_elastic("thing", "/thing", "1.2"))

    def test_select_fields(self):
        results = self.search_manager.search({
            "artifactName": {
                "searchType": SearchType.MATCH,
                "value": "test"
            }
        }, ["artifactPath"])
        print results["test"]
        self.assertEqual(results, {"test": [{"name": "artifactPath", "value": "test", "immutable": True}]})
