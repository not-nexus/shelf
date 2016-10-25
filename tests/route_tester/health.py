from tests.route_tester.base import Base


class Canary(Base):
    def __init__(self, test, test_client):
        super(Canary, self).__init__(test, test_client)
        self.route = "/canary"
