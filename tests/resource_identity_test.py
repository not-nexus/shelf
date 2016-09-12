import pyproctor
from pyshelf.resource_identity import ResourceIdentity
from mock import Mock
from pyshelf.resource_identity_factory import ResourceIdentityFactory


class ResourceIdentityTest(pyproctor.TestBase):
    TEST_PATH = "/lol-test/artifact/blah1/blah2/blah3"

    def create(self):
        return ResourceIdentity(self.TEST_PATH)

    def test_bucket_name(self):
        identity = self.create()
        self.assertEqual("lol-test", identity.bucket_name)

    def test_artifact_path(self):
        identity = self.create()
        self.assertEqual("/blah1/blah2", identity.artifact_path)

    def test_cloud(self):
        self.assertEqual("/blah1/blah2/blah3", self.create().cloud)

    def test_search(self):
        self.assertEqual("5a61d333034c1bde88bf01f7380796a40cc4b2ad9d7358e826bc414bfa75c3ad", self.create().search)

    def test_cloud_metatdata(self):
        self.assertEquals("/blah1/blah2/_metadata_blah3.yaml", self.create().cloud_metadata)

    def test_cloud_metadata_special_type(self):
        url = ResourceIdentityTest.TEST_PATH + "/_meta"
        identity = ResourceIdentity(url)
        self.assertEqual("/blah1/blah2/_metadata_blah3.yaml", identity.cloud_metadata)

    def test_cloud_metadata_special_type_with_item(self):
        url = ResourceIdentityTest.TEST_PATH + "/_meta/item_lol"
        identity = ResourceIdentity(url)
        self.assertEqual("/blah1/blah2/_metadata_blah3.yaml", identity.cloud_metadata)

    def test_multiple_separators_and_no_leading_slash(self):
        identity = ResourceIdentity("lol-test//artifact///blah1//blah2")
        self.assertEqual("/blah1", identity.artifact_path)
        self.assertEqual("lol-test", identity.bucket_name)

    def test_artifact_name(self):
        self.assertEqual("blah3", self.create().artifact_name)

    def test_resource_path(self):
        self.assertEqual("/lol-test/artifact/blah1/blah2/blah3", self.create().resource_path)

    def test_artifact_name_with_search(self):
        self.run_artifact_name_with_alternate_suffix("_search")

    def test_artifact_name_with_meta(self):
        self.run_artifact_name_with_alternate_suffix("_meta")

    def run_artifact_name_with_alternate_suffix(self, suffix):
        path = ResourceIdentityTest.TEST_PATH + "/" + suffix
        identity = ResourceIdentity(path)
        self.assertEqual("blah3", identity.artifact_name)

    def test_multiple_meta(self):
        path = "_meta/lol/_meta"
        identity = ResourceIdentity(path)
        self.assertEqual([''], identity._part_list)

    def test_resource_id_factory_from_cloud_id(self):
        path_converter_mock = Mock()
        path_converter_mock.from_cloud_metadata = Mock(return_value="ref/artifact/test/_metadata_test.yaml")
        id_factory = ResourceIdentityFactory(path_converter_mock)
        identity = id_factory.from_cloud_metadata_identifier("ref/artifact/test/_meta")
        self.assertEqual("ref", identity.bucket_name)
        self.assertEqual("/test", identity.artifact_path)
