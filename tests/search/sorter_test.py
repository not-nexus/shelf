from tests.unit_test_base import UnitTestBase
from pyshelf.search.sort_flag import SortFlag
from pyshelf.search.sort_type import SortType
import tests.metadata_utils as utils
from pyshelf.search.sorter import Sorter


class SorterTest(UnitTestBase):
    def setUp(self):
        super(SorterTest, self).setUp()
        self.sorter = Sorter()

    def test_sorted_desc_and_asc(self):
        sort = [
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
            },
        ]

        data = [
            utils.get_meta("zzzz", "/zzzz", "1.19"),
            utils.get_meta("a", "/a", "1.19"),
            utils.get_meta("thing", "/thing", "1.2"),
            utils.get_meta("blah", "/blah", "1.19"),
        ]

        results = self.sorter.sort(data, sort)

        expected = [
            utils.get_meta("a", "/a", "1.19"),
            utils.get_meta("blah", "/blah", "1.19"),
            utils.get_meta("zzzz", "/zzzz", "1.19"),
            utils.get_meta("thing", "/thing", "1.2"),
        ]
        self.asserts.json_equals(expected, results)

    def test_tilde_sort(self):
        sort = [
            {
                "field": "version",
                "sort_type": SortType.ASC,
                "flag_list": [
                    SortFlag.VERSION
                ]
            }
        ]

        data = [
            utils.get_meta("a", "/a", "1.19"),
            utils.get_meta("blah", "/blah", "1.19"),
            utils.get_meta("thing", "/thing", "1.2"),
            utils.get_meta("other", "/this/that/other", "1.1"),
            utils.get_meta("zzzz", "/zzzz", "1.19")
        ]

        results = self.sorter.sort(data, sort)

        expected = [
            utils.get_meta("other", "/this/that/other", "1.1"),
            utils.get_meta("thing", "/thing", "1.2"),
            utils.get_meta("a", "/a", "1.19"),
            utils.get_meta("blah", "/blah", "1.19"),
            utils.get_meta("zzzz", "/zzzz", "1.19")
        ]
        self.asserts.json_equals(expected, results)
