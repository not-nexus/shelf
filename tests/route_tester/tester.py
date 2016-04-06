from tests.route_tester.metadata import Metadata
from tests.route_tester.metadata_item import MetadataItem
from tests.route_tester.artifact import Artifact
from tests.route_tester.search import Search

class Tester(object):
    def __init__(self, test, test_client):
        self.test = test
        self.test_client = test_client

    def metadata(self):
        return Metadata(self.test, self.test_client)

    def metadata_item(self):
        return MetadataItem(self.test, self.test_client)

    def artifact(self):
        return Artifact(self.test, self.test_client)

    def search(self):
        return Search(self.test, self.test_client)
