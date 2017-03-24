from tests.unit_test_base import UnitTestBase
from shelf.search.sort_flag import SortFlag
from shelf.search.sort_type import SortType
import tests.metadata_utils as utils
from shelf.search.sorter import Sorter
from copy import deepcopy


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

    def test_version_sort_missing_property(self):
        sort = [
            {
                "field": "buildNumber",
                "sort_type": SortType.DESC,
                "flag_list": [
                    SortFlag.VERSION
                ]
            }
        ]

        data = [
            {
                "nothing": {
                    "name": "nothing",
                    "value": "stuff",
                    "immutable": True
                }
            },
            {
                "buildNumber": {
                    "name": "buildNumber",
                    "value": "187",
                    "immutable": True
                }
            },
            {
                "buildNumber": {
                    "name": "buildNumber",
                    "value": "205",
                    "immutable": True
                }
            }
        ]

        # Descending sort test with missing property
        # rather then returning `None` version sorts return
        # "0" as that acts as `None` does with version sorts.
        results = self.sorter.sort(data, sort)
        expected = deepcopy(data)
        self.asserts.json_equals(expected, results)

        # Ascending sort test making sure both directions with
        # versions work properly with a missing property.
        sort[0]["sort_type"] = SortType.ASC
        asc_results = self.sorter.sort(data, sort)
        expected.reverse()
        self.asserts.json_equals(expected, asc_results)

    def test_integer_version_sort(self):
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
            utils.get_meta("a", "/a", 3),
            utils.get_meta("blah", "/blah", 2),
            utils.get_meta("thing", "/thing", 1),
            utils.get_meta("zzzz", "/zzzz", 2)
        ]
        results = self.sorter.sort(data, sort)
        expected = [
            utils.get_meta("thing", "/thing", 1),
            utils.get_meta("blah", "/blah", 2),
            utils.get_meta("zzzz", "/zzzz", 2),
            utils.get_meta("a", "/a", 3)
        ]
        self.asserts.json_equals(expected, results)

    def test_none_version_sort(self):
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
            utils.get_meta("thing", "/thing", 2),
            utils.get_meta("blah", "/blah", "1"),
            utils.get_meta("a", "/a", None),
            utils.get_meta("zzzz", "/zzzz", "12.2.0")
        ]
        results = self.sorter.sort(data, sort)
        expected = [
            utils.get_meta("a", "/a", None),
            utils.get_meta("blah", "/blah", "1"),
            utils.get_meta("thing", "/thing", 2),
            utils.get_meta("zzzz", "/zzzz", "12.2.0")
        ]
        self.asserts.json_equals(expected, results)
