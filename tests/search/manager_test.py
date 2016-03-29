from tests.unit_test_base import UnitTestBase
from tests.search.test_wrapper import TestWrapper as SearchTestWrapper
from pyshelf.search.type import Type as SearchType
from pyshelf.search.sort_type import SortType
from pyshelf.search.sort_flag import SortFlag
import tests.metadata_utils as utils
import time


class ManagerTest(UnitTestBase):
    def setUp(self):
        self.test_wrapper = SearchTestWrapper()
        self.search_manager = self.test_wrapper.search_container.search_manager
        self.test_wrapper.setup_metadata()
        self.test_wrapper.setup_metadata("other", "/this/that/other", "1.1")
        self.test_wrapper.setup_metadata("thing", "/thing", "1.2")
        self.test_wrapper.setup_metadata("blah", "/blah", "1.19")
        self.test_wrapper.setup_metadata("a", "/a", "1.19")
        self.test_wrapper.setup_metadata("zzzz", "/zzzz", "1.19")
        # temp fix
        time.sleep(1)

    def tearDown(self):
        self.test_wrapper.teardown_metadata("test")
        self.test_wrapper.teardown_metadata("other")
        self.test_wrapper.teardown_metadata("thing")

    def test_equality_search(self):
        results = self.search_manager.search({
            "search": [
                {
                    "field": "artifactName",
                    "search_type": SearchType.MATCH,
                    "value": "test"
                },
                {
                    "field": "artifactPath",
                    "search_type": SearchType.WILDCARD,
                    "value": "tes?"
                }
            ]
        })
        expected = [utils.get_meta()]
        self.assertEqual(results, expected)

    def test_tilde_search_and_sort(self):
        results = self.search_manager.search({
            "search": [
                {
                    "field": "version",
                    "search_type": SearchType.TILDE,
                    "value": "1.1"
                }
            ],
            "sort": [
                {
                    "field": "version",
                    "sort_type": SortType.ASC,
                    "flag_list": [
                        SortFlag.VERSION
                    ]
                },
            ]
        })
        expected = [
            utils.get_meta("other", "/this/that/other", "1.1"),
            utils.get_meta("thing", "/thing", "1.2"),
            utils.get_meta("a", "/a", "1.19"),
            utils.get_meta("zzzz", "/zzzz", "1.19"),
            utils.get_meta("blah", "/blah", "1.19")
        ]
        self.assertEqual(results, expected)

    def test_select_fields(self):
        results = self.search_manager.search({
            "search": [
                {
                    "field": "artifactName",
                    "search_type": SearchType.MATCH,
                    "value": "test"
                }
            ]
        }, ["artifactPath"])
        self.assertEqual(results[0], {"artifactPath": {"name": "artifactPath", "value": "test", "immutable": True}})

    def test_dumb_tilde_search(self):
        results = self.search_manager.search({
            "search": [
                {
                    "field": "artifactName",
                    "search_type": SearchType.TILDE,
                    "value": "test"
                }
            ],
            "sort": [
                {
                    "field": "artifactName",
                    "sort_type": SortType.DESC
                }
            ]
        })
        self.maxDiff = None
        expected = [
            utils.get_meta("zzzz", "/zzzz", "1.19"),
            utils.get_meta("thing", "/thing", "1.2"),
            utils.get_meta()
        ]

        self.assertEqual(results, expected)

    def test_sorted_desc_and_asc(self):
        results = self.search_manager.search({
            "search": [
                {
                    "field": "version",
                    "search_type": SearchType.TILDE,
                    "value": "1.2"
                }
            ],
            "sort": [
                {
                    "field": "version",
                    "sort_type": SortType.DESC,
                    "flag_list": [
                        SortFlag.VERSION
                    ]
                },
                {
                    "field": "artifactName",
                    "sort_type": SortType.ASC
                }
            ]
        })
        expected = [
            utils.get_meta("a", "/a", "1.19"),
            utils.get_meta("blah", "/blah", "1.19"),
            utils.get_meta("zzzz", "/zzzz", "1.19"),
            utils.get_meta("thing", "/thing", "1.2")
        ]
        self.assertEqual(results, expected)
