from tests.unit_test_base import UnitTestBase
from pyshelf.search_parser import SearchParser
from pyshelf.search.sort_type import SortType
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
                    "search_type": SearchType.TILDE
                }
            ],
            "sort": [
                {
                    "field": "version",
                    "sort_type": SortType.VERSION,
                    "flag_list": [SortType.DESC]
                }
            ],
            "limit": 1
        }
        criteria = self.parser.from_request(request_criteria)
        self.assertEqual(criteria, expected)

    def test_from_request_lists(self):
        request_criteria = {
            "search": [
                "version~=1.1",
                "bob=bob",
                "dumb*=dumbf*"
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
                    "search_type": SearchType.TILDE
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
                }
            ],
            "sort": [
                {
                    "field": "version",
                    "sort_type": SortType.VERSION,
                    "flag_list": [SortType.ASC]
                },
                {
                    "field": "bob",
                    "flag_list": [SortType.ASC]
                }
            ],
            "limit": None
        }
        criteria = self.parser.from_request(request_criteria)
        self.assertEqual(criteria, expected)
