from tests.unit_test_base import UnitTestBase
from tests.search.test_wrapper import TestWrapper as SearchTestWrapper
from pyshelf.search.type import Type as SearchType
from pyshelf.search.sort_type import SortType
from pyshelf.search.sort_flag import SortFlag
import tests.metadata_utils as utils
from pyshelf.search.metadata import Metadata


class ManagerTest(UnitTestBase):
    def setUp(self):
        super(ManagerTest, self).setUp()
        self.test_wrapper = SearchTestWrapper(self.search_container)
        self.search_manager = self.search_container.search_manager
        data = [
            utils.get_meta(),
            utils.get_meta("other", "/this/that/other", "1.1"),
            utils.get_meta("thing", "/thing", "1.2"),
            utils.get_meta("blah", "/blah", "1.19"),
            utils.get_meta("a", "/a", "1.19"),
            utils.get_meta("zzzz", "/zzzz", "1.19"),
        ]
        self.test_wrapper.setup_metadata(data)

    def tearDown(self):
        self.test_wrapper.teardown_metadata()

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

    def test_no_match(self):
        results = self.search_manager.search({
            "search": [
                {
                    "field": "artifactName",
                    "search_type": SearchType.MATCH,
                    "value": "neverrrrrrgonnamattttch"
                }
            ]
        })
        self.assertEqual(results, [])

    def test_tilde_search_and_sort(self):
        results = self.search_manager.search({
            "search": [
                {
                    "field": "version",
                    "search_type": SearchType.VERSION,
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
        self.maxDiff = None
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
                    "search_type": SearchType.VERSION,
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
                    "search_type": SearchType.VERSION,
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
