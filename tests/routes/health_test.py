from mock import Mock
from pyshelf.health_status import HealthStatus
from pyshelf.search.manager import Manager as SearchManager
from tests.functional_test_base import FunctionalTestBase
import requests
from pyproctor import MonkeyPatcher


class HealthTest(FunctionalTestBase):
    def test_ok(self):
        self.route_tester \
            .health() \
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

    def test_connection_failure_to_search(self):
        # Sabotage search so that I can force the API to be
        # unhealthy.
        search = Mock(side_effect=requests.ConnectionError())
        MonkeyPatcher.patch(SearchManager, "search", search)

        self.route_tester \
            .search() \
            .route_params(bucket_name="test", path="") \
            .expect(500) \
            .post(headers=self.auth)

        self.route_tester \
            .health() \
            .expect(
                503,
                {
                    "status": HealthStatus.CRITICAL,
                    "search": False,
                    "failingStorage": [],
                    "passingStorage": [
                        "b2",
                        "test",
                        "thisBucketDoesntExistLol",
                    ]
                }
            ) \
            .get()

        # A successful request to search should make the endpoint
        # be healthy again.

        # Reset the sabotage I did earlier.
        MonkeyPatcher.reset()
        self.route_tester \
            .search() \
            .route_params(bucket_name="test", path="") \
            .expect(204) \
            .post(headers=self.auth)

        self.route_tester \
            .health() \
            .expect(
                200,
                {
                    "status": HealthStatus.OK,
                    "search": True,
                    "failingStorage": [],
                    "passingStorage": [
                        "b2",
                        "test",
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
            .health() \
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
