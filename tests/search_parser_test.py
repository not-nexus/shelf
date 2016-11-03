from tests.unit_test_base import UnitTestBase
from shelf.search_parser import SearchParser
from shelf.search.sort_type import SortType
from shelf.search.sort_flag import SortFlag
from shelf.search.type import Type as SearchType
import tests.metadata_utils as utils
from shelf.search_portal import SearchPortal
from mock import Mock


class SearchParserTest(UnitTestBase):
    def setUp(self):
        self.parser = SearchParser()
        self.portal = SearchPortal(Mock())

    def test_from_request(self):
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
        criteria = self.parser.from_request(request_criteria)
        self.assertEqual(expected, criteria)

    def test_listing(self):
        results = []
        expected = ["dir/test"]

        for i in range(5):
            results.append(utils.get_meta(path="/test/artifact/dir/test"))

        parsed = self.portal._list_artifacts(results, 1)
        self.assertEqual(expected, parsed)

    def test_version_search_string(self):
        expected = {
            "field": "test\~\=ing",
            "value": "1.1",
            "search_type": SearchType.VERSION
        }
        self.assert_search_criteria("test\~\=ing~=1.1", expected)

    def test_equality_search_string(self):
        expected = {
            "field": "test\=ing",
            "value": "1.1",
            "search_type": SearchType.MATCH
        }
        self.assert_search_criteria("test\=ing=1.1", expected)

    def test_fake_wildcard_actually_match_search_string(self):
        expected = {
            "field": "test\=i\*ng",
            "value": "1.1",
            "search_type": SearchType.MATCH
        }
        self.assert_search_criteria("test\=i\*ng=1.1", expected)

    def assert_search_criteria(self, search_string, expected):
        formatted = self.parser._format_search_criteria(search_string)
        self.assertEqual(expected, formatted)
