from tests.unit_test_base import UnitTestBase
from pyshelf.search_parser import SearchParser
from pyshelf.search.sort_type import SortType
from pyshelf.search.sort_flag import SortFlag
from pyshelf.search.type import Type as SearchType


class SearchParseTest(UnitTestBase):
    def setUp(self):
        self.parser = SearchParser()

    def test_from_request_singular(self):
        self.maxDiff = None
        request_criteria = {
            "search": "version~=1.1",
            "sort": "version, VERSION, DESC",
            "limit": 1
        }
        expected = {
            "search": [
                {
                    "field": "version",
                    "value": "1.1",
                    "search_type": SearchType.VERSION
                },
                {
                    "field": "artifactPath",
                    "value": "*",
                    "search_type": SearchType.WILDCARD
                }
            ],
            "sort": [
                {
                    "field": "version",
                    "sort_type": SortType.DESC,
                    "flag_list": [SortFlag.VERSION]
                }
            ]
        }
        criteria = self.parser.from_request(request_criteria, "")
        self.assertEqual(criteria, expected)

    def test_from_request_lists(self):
        request_criteria = {
            "search": [
                "version~=1.1",
                "bob=bob",
                "dumb=dumbf*"
            ],
            "sort": [
                "version, VERSION, ASC",
                "bob, ASC"
            ]
        }
        expected = {
            "search": [
                {
                    "field": "version",
                    "value": "1.1",
                    "search_type": SearchType.VERSION
                },
                {
                    "field": "bob",
                    "value": "bob",
                    "search_type": SearchType.MATCH
                },
                {
                    "field": "dumb",
                    "value": "dumbf*",
                    "search_type": SearchType.WILDCARD
                },
                {
                    "field": "artifactPath",
                    "value": "test*",
                    "search_type": SearchType.WILDCARD
                }
            ],
            "sort": [
                {
                    "field": "version",
                    "sort_type": SortType.ASC,
                    "flag_list": [SortFlag.VERSION]
                },
                {
                    "field": "bob",
                    "sort_type": SortType.ASC
                }
            ]
        }
        criteria = self.parser.from_request(request_criteria, "test")
        self.assertEqual(criteria, expected)
