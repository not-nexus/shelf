from tests.unit_test_base import UnitTestBase
from tests.search.search_test_wrapper import SearchTestWrapper
from pyshelf.search.type import Type as SearchType
import tests.metadata_utils as utils
import time


class ManagerTest(UnitTestBase):
    def setUp(self):
        self.test_wrapper = SearchTestWrapper()
        self.search_manager = self.test_wrapper.search_manager
        self.test_wrapper.setup_metadata("test")
        self.test_wrapper.setup_metadata("other", "other", "/this/that/other", "1.1")
        time.sleep(1)

    def tearDown(self):
        self.test_wrapper.teardown_metadata("test")
        self.test_wrapper.teardown_metadata("other")

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
        self.assertEqual(len(results.hits), 1)
        self.assertEqual(results.hits[0].items, utils.get_meta_elastic()["items"])

    def test_tilde_search(self):
        results = self.search_manager.search({
            "version": {
                "searchType": SearchType.TILDE,
                "value": "1.1"
            }
        })
        self.assertEqual(len(results.hits), 1)
        self.assertEqual(results.hits[0].items, utils.get_meta_elastic("other", "/this/that/other", "1.1")["items"])
