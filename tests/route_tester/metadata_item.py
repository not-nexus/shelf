from tests.route_tester.base import Base


class MetadataItem(Base):
    def __init__(self, test, test_client):
        Base.__init__(self, test, test_client)
        self.route = "/artifact/{path}/_meta/{item}"
