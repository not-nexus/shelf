from tests.route_tester.base import Base


class Health(Base):
    def __init__(self, test, test_client):
        super(Health, self).__init__(test, test_client)
        self.route = "/health"
