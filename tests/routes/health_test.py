from mock import Mock
from pyproctor import MonkeyPatcher
from shelf.health_status import HealthStatus
from shelf.search.manager import Manager as SearchManager
from tests.functional_test_base import FunctionalTestBase
import requests
import tests.permission_utils as utils


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
                    "search": True,
                    "failingStorage": [],
                    "passingStorage": [
                        "b2",
                        "test",
                        # This one is a bit wierd but sort of illustrates how the health check works. It is
                        # decided to be healthy unless it failed to connect.
                        "thisBucketDoesntExistLol",
                    ]
                },
                {
                    "X-Status": HealthStatus.OK
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

        # Now make it exist suddenly so we can see it fixes the health.
        self.boto_connection.create_bucket("this-bucket-doesnt-exist-lol")
        self.add_auth_token(utils.VALID_TOKEN, "this-bucket-doesnt-exist-lol")

        self.route_tester \
            .search() \
            .route_params(bucket_name="thisBucketDoesntExistLol", path="") \
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

    def test_bucket_not_configured_does_not_cause_a_failure(self):
        self.route_tester \
            .search() \
            .route_params(bucket_name="some-not-configured-bucket", path="") \
            .expect(404) \
            .post(headers=self.auth)

        self.assert_health_ok()

    def test_artifact_not_found_does_not_cause_a_failure(self):
        self.route_tester \
            .artifact() \
            .route_params(bucket_name="test", path="nada") \
            .expect(404) \
            .get(headers=self.auth)

        self.assert_health_ok()
