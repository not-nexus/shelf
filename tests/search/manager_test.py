from tests.unit_test_base import UnitTestBase
from tests.search.search_test_wrapper import SearchTestWrapper
from pyshelf.search.type import Type as SearchType
import tests.metadata_utils as utils
import json


class ManagerTest(UnitTestBase):
    def setUp(self):
        self.test_wrapper = SearchTestWrapper()
        self.search_manager = self.test_wrapper.search_manager
        self.test_wrapper.setup_metadata("test")
        self.test_wrapper.setup_metadata("other", "other", "/this/that/other")

    def test_equality_search(self):
        results = self.search_manager.search({
            "artifactName": {
                "searchType": SearchType.MATCH,
                "value": "test"
            },
            "artifactPath": {
                "searchType": SearchType.WILDCARD,
                "value": "te*"
            }
        })
        for hit in results.hits:
            self.assertEqual(hit.items, utils.get_meta_elastic()["items"])
        self.assertEqual(len(results.hits), 1)
