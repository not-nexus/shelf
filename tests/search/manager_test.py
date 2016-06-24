from tests.unit_test_base import UnitTestBase
from tests.search.test_wrapper import TestWrapper as SearchTestWrapper
from pyshelf.search.type import Type as SearchType
from pyshelf.search.sort_type import SortType
from pyshelf.search.sort_flag import SortFlag
from pyshelf.search.connection import Connection
import tests.metadata_utils as utils


class ManagerTest(UnitTestBase):
    def setUp(self):
        super(ManagerTest, self).setUp()
        self.test_wrapper = SearchTestWrapper(self.search_container)
        self.manager = self.search_container.manager
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
        results = self.manager.search({
            "search": [
                {
                    "field": "artifactName",
                    "search_type": SearchType.MATCH,
                    "value": "test"
                },
                {
                    "field": "artifactPath",
                    "search_type": SearchType.WILDCARD,
                    "value": "/test/artifact/tes?"
                }
            ]
        })
        expected = [utils.get_meta()]
        self.assertEqual(expected, results)

    def test_no_match(self):
        results = self.manager.search({
            "search": [
                {
                    "field": "artifactName",
                    "search_type": SearchType.MATCH,
                    "value": "neverrrrrrgonnamattttch"
                }
            ]
        })
        self.assertEqual([], results)

    def test_tilde_search_and_sort(self):
        results = self.manager.search({
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
            utils.get_meta("blah", "/blah", "1.19"),
            utils.get_meta("zzzz", "/zzzz", "1.19")
        ]
        self.asserts.json_equals(expected, results)

    def test_select_fields(self):
        results = self.manager.search({
            "search": [
                {
                    "field": "artifactName",
                    "search_type": SearchType.MATCH,
                    "value": "test"
                }
            ]
        }, ["artifactPath"])
        self.assertEqual({"artifactPath": {"name": "artifactPath", "value": "/test/artifact/test",
            "immutable": True}}, results[0])

    def test_dumb_tilde_search(self):
        results = self.manager.search({
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

        self.assertEqual(expected, results)

    def test_sorted_desc_and_asc(self):
        results = self.manager.search({
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
        self.assertEqual(expected, results)

    def test_more_then_ten_results(self):
        data = []

        # In setup 6 documents have already been added. Making an even 20.
        for i in range(14):
            data.append(utils.get_meta("mutli-test{0}".format(str(i))))

        self.test_wrapper.setup_metadata(data)
        results = self.manager.search({
            "search": [{
                "field": "artifactName",
                "search_type": SearchType.WILDCARD,
                "value": "*"
            }]
        })
        self.assertEqual(20, len(results))

    def test_utils(self):
        connection = Connection("http://localhost:9200/index", "test", "test", "test")
        host = connection.transport.hosts[0]
        self.assertEqual("localhost", host["host"])
        self.assertEqual(9200, host["port"])
        self.assertEqual("index", connection.es_index)
        auth = connection.transport.get_connection().session.auth
        self.assertEqual("test", auth.aws_access_key)
        self.assertEqual("test", auth.aws_secret_access_key)
        self.assertEqual("localhost", auth.aws_host)
        self.assertEqual("test", auth.aws_region)
