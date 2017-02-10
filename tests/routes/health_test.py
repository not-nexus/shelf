from shelf.health_status import HealthStatus
from tests.functional_test_base import FunctionalTestBase


class HealthTest(FunctionalTestBase):
    def assert_health_ok(self):
        self.route_tester \
            .health() \
            .expect(200) \
            .get()

    def test_ok(self):
        self.route_tester \
            .health() \
            .expect(
                200,
                {
                    "status": HealthStatus.OK,
                },
                {
                    "X-Status": HealthStatus.OK
                }
            ) \
            .get()
