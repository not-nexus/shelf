import shelf.artifact_key_filter as akfilter
from tests.unit_test_base import UnitTestBase


class ArtifactKeyFilterTest(UnitTestBase):
    def key(self, name):
        key = type("FakeKey", (object,), {})()
        key.name = name
        return key

    def run_is_private(self, name, result=True):
        self.assertEquals(result, akfilter._is_private(name))

    def test_to_path_list(self):
        key_list = [
            self.key("/hello"),
            self.key("/hello/goodbye")
        ]

        expected_list = [
            "/hello",
            "/hello/goodbye"
        ]

        actual_list = akfilter.to_path_list(key_list)
        self.assertEqual(expected_list, actual_list)

    def test_is_private_keys(self):
        self.run_is_private("_keys")

    def test_is_private_metadata(self):
        self.run_is_private("/blah/lol/_metadata_whatever", False)

    def test_is_private_other(self):
        self.run_is_private("/blah/_metajustkidding_whatever")

    def test_is_private_other_dir(self):
        self.run_is_private("/blah/_hello/hi")

    def test_private(self):
        path_list = [
            "/sup/_man",
            "/blah/hello",
            "_keys/kyle",
            "/this/one/fine",
            "/blah/_metadata_20",
        ]

        expected_list = [
            "/blah/hello",
            "/this/one/fine",
            "/blah/_metadata_20",
        ]

        filtered_path_list = akfilter.private(path_list)
        self.assertEqual(expected_list, filtered_path_list)

    def test_metadata(self):
        path_list = [
            "/blah/_metadata_20",
            "_key/blah",
            "/blah/_blah/_more_blah",
        ]

        expected_list = [
            "_key/blah",
            "/blah/_blah/_more_blah",
        ]

        filtered_path_list = akfilter.metadata(path_list)
        self.assertEqual(expected_list, filtered_path_list)

    def test_not_metadata(self):
        path_list = [
            "/blah/_metadata_20",
            "_key/blah",
            "/blah/_blah/_more_blah",
        ]

        expected_list = [
            "/blah/_metadata_20",
        ]

        filtered_path_list = akfilter.not_metadata(path_list)
        self.assertEqual(expected_list, filtered_path_list)

    def test_all_private(self):
        path_list = [
            "/sup/_man",
            "/blah/hello",
            "_keys/kyle",
            "/this/one/fine",
            "/blah/_metadata_20",
        ]

        expected_list = [
            "/blah/hello",
            "/this/one/fine",
        ]

        filtered_path_list = akfilter.all_private(path_list)
        self.assertEqual(expected_list, filtered_path_list)

    def test_directories(self):
        path_list = [
            "/sup",
            "directory1/",
            "/blah/hello",
            "directory2/",
        ]

        expected_list = [
            "/sup",
            "/blah/hello"
        ]

        filtered_path_list = akfilter.directories(path_list)
        self.assertEqual(expected_list, filtered_path_list)
