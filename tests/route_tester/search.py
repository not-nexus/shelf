from tests.route_tester.base import Base


class Search(Base):
    def __init__(self, test, test_client):
        Base.__init__(self, test, test_client)
        self.route = "/{bucket_name}/artifact/{path}/_search"
