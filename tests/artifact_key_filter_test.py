import pyshelf.artifact_key_filter as akfilter
from tests.unit_test_base import UnitTestBase


class ArtifactKeyFilterTest(UnitTestBase):
    def key(self, name):
        key = type("FakeKey", (object,), {})()
        key.name = name
        return key

    def run_is_private(self, name, result=True):
        self.assertEquals(result, akfilter._is_private(self.key(name)))

    def test_is_private_keys(self):
        self.run_is_private("_keys")

    def test_is_private_metadata(self):
        self.run_is_private("/blah/lol/_metadata_whatever", False)

    def test_is_private_other(self):
        self.run_is_private("/blah/_metajustkidding_whatever")

    def test_is_private_other_dir(self):
        self.run_is_private("/blah/_hello/hi")

    def assert_keys_match(self, expected_name_list, filtered_key_list):
        filtered_name_list = [key.name for key in filtered_key_list]
        self.assertEqual(expected_name_list, filtered_name_list)

    def test_private(self):
        key_list = [
            self.key("/sup/_man"),
            self.key("/blah/hello"),
            self.key("_keys/kyle"),
            self.key("/this/one/fine"),
            self.key("/blah/_metadata_20"),
        ]

        expected_list = [
            "/blah/hello",
            "/this/one/fine",
            "/blah/_metadata_20",
        ]

        filtered_key_list = akfilter.private(key_list)
        self.assert_keys_match(expected_list, filtered_key_list)

    def test_metadata(self):
        key_list = [
            self.key("/blah/_metadata_20"),
            self.key("_key/blah"),
            self.key("/blah/_blah/_more_blah"),
        ]

        expected_list = [
            "_key/blah",
            "/blah/_blah/_more_blah",
        ]

        filtered_key_list = akfilter.metadata(key_list)
        self.assert_keys_match(expected_list, filtered_key_list)

    def test_not_metadata(self):
        key_list = [
            self.key("/blah/_metadata_20"),
            self.key("_key/blah"),
            self.key("/blah/_blah/_more_blah"),
        ]

        expected_list = [
            "/blah/_metadata_20",
        ]

        filtered_key_list = akfilter.not_metadata(key_list)
        self.assert_keys_match(expected_list, filtered_key_list)

    def test_all_private(self):
        key_list = [
            self.key("/sup/_man"),
            self.key("/blah/hello"),
            self.key("_keys/kyle"),
            self.key("/this/one/fine"),
            self.key("/blah/_metadata_20"),
        ]

        expected_list = [
            "/blah/hello",
            "/this/one/fine",
        ]

        filtered_key_list = akfilter.all_private(key_list)
        self.assert_keys_match(expected_list, filtered_key_list)
