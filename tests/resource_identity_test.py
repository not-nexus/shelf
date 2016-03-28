import pyproctor
from pyshelf.resource_identity import ResourceIdentity


class ResourceIdentityTest(pyproctor.TestBase):
    TEST_PATH = "/lol-test/artifact/blah1/blah2/blah3"

    def create(self):
        return ResourceIdentity(self.TEST_PATH)

    def test_bucket_name(self):
        identity = self.create()
        self.assertEqual("lol-test", identity.bucket_name)

    def test_artifact_path(self):
        identity = self.create()
        self.assertEqual("/blah1/blah2/blah3", identity.artifact_path)

    def test_cloud(self):
        self.assertEqual("/blah1/blah2/blah3", self.create().cloud)

    def test_search(self):
        self.assertEqual("abc0068b8b6cdd87550a4fc0cb5b7dc538c51c9ca50d5e5f9f4f2f08fc80e24e", self.create().search)

    def test_cloud_metatdata(self):
        self.assertEquals("/blah1/blah2/blah3/_meta", self.create().cloud_metadata)

    def test_cloud_metadata_special_type(self):
        url = ResourceIdentityTest.TEST_PATH + "/_meta"
        identity = ResourceIdentity(url)
        self.assertEqual("/blah1/blah2/blah3/_meta", identity.cloud_metadata)

    def test_cloud_metadata_special_type_with_item(self):
        url = ResourceIdentityTest.TEST_PATH + "/_meta/item_lol"
        identity = ResourceIdentity(url)
        self.assertEqual("/blah1/blah2/blah3/_meta", identity.cloud_metadata)

    def test_multiple_separators_and_no_leading_slash(self):
        identity = ResourceIdentity("lol-test//artifact///blah1//blah2")
        self.assertEqual("/blah1/blah2", identity.artifact_path)
        self.assertEqual("lol-test", identity.bucket_name)

    def test_artifact_name(self):
        self.assertEqual("blah3", self.create().artifact_name)

    def test_artifact_name_with_search(self):
        self.run_artifact_name_with_alternate_suffix("_search")

    def test_artifact_name_with_meta(self):
        self.run_artifact_name_with_alternate_suffix("_meta")

    def run_artifact_name_with_alternate_suffix(self, suffix):
        path = ResourceIdentityTest.TEST_PATH + "/" + suffix
        identity = ResourceIdentity(path)
        self.assertEqual("blah3", identity.artifact_name)
