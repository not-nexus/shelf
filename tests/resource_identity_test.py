import pyproctor
from pyshelf.resource_identity import ResourceIdentity


class ResourceIdentityTest(pyproctor.TestBase):
    TEST_PATH = "/lol-test/artifact/blah1/blah2/blah3"

    def create(self):
        return ResourceIdentity(self.TEST_PATH)

    def test_bucket_name(self):
        identity = self.create()
        self.assertEqual("lol-test", identity.bucket_name)

    def test_path(self):
        identity = self.create()
        self.assertEqual("/blah1/blah2/blah3", identity.path)
