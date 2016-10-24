from tests.functional_test_base import FunctionalTestBase
from pyshelf.health_status import HealthStatus


class CanaryTest(FunctionalTestBase):
    def test_ok(self):
        self.route_tester \
            .canary() \
            .expect(
                200,
                {
                    "status": HealthStatus.OK,
                    "search": True,
                    "failingStorage": [],
                    "passingStorage": [
                        "b2",
                        "test",
                        # This one is a bit wierd but sort of illustrates how the health check works. It is
                        # decided to be healthy unless it failed to connect.
                        "thisBucketDoesntExistLol",
                    ]
                }
            ) \
            .get()

    def test_failure_for_non_existent_bucket(self):
        self.fail("Incomplete functionality.  Cannot test it yet")  # TODO: Remove this when other tasks are complete

        self.route_tester \
            .search() \
            .route_params(bucket_name="thisBucketDoesntExistLol", path="") \
            .expect(500) \
            .post(headers=self.auth)

        self.route_tester \
            .canary() \
            .expect(
                503,
                {
                    "status": HealthStatus.CRITICAL,
                    "search": True,
                    "failingStorage": [
                        "thisBucketDoesntExistLol",
                    ],
                    "passingStorage": [
                        "b2",
                        "test",
                    ]
                }
            ) \
            .get()
