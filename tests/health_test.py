from tests.test_base import TestBase
from pyshelf.health import Health
from pyshelf.health_status import HealthStatus


class HealthTest(TestBase):
    def setUp(self):
        super(HealthTest, self).setUp()
        self.config = {
            "buckets": [
                {
                    "refName": "hi"
                },
                {
                    "refName": "hello"
                },
                {
                    "refName": "other"
                },
                {
                    "refName": "four",
                },
                {
                    "refName": "five"
                }
            ]
        }
        self.health = Health(self.config)

    def test_get_failing_ref_name_list(self):
        self.health.refNames = {
            "hi": False,
            "hello": True,
            "other": False,
        }

        expected = [
            "hi",
            "other"
        ]

        actual = self.health.get_failing_ref_name_list()
        # I sort them because the order in which dictionaries will iterate
        # through items is not reliable by design.
        self.assertEqual(sorted(expected), sorted(actual))

    def test_get_passing_ref_name_list(self):
        self.health.refNames = {
            "hello": False
        }

        expected = [
            "hi",
            "other",
            "four",
            "five"
        ]

        actual = self.health.get_passing_ref_name_list()
        self.assertEqual(sorted(expected), sorted(actual))

    def run_get_status(self, elasticsearch, refNames, expected):
        self.health.refNames = refNames
        self.health.elasticsearch = elasticsearch
        status = self.health.get_status()
        self.assertEqual(expected, status)

    def test_get_status_20_percent_failing_bucket(self):
        self.run_get_status(
            True,
            {
                "four": False,
                "five": True,  # Just for fun, shouldn't break anything.
            },
            HealthStatus.CRITICAL
        )

    def test_get_status_less_than_20_percent_failing_bucket(self):
        # I have to inflate the number of total buckets so that
        # I can have more than 0% but less than 20% failing.
        self.config["buckets"].append({
            "refName": "six"
        })

        self.run_get_status(
            True,
            {
                "four": False,
            },
            HealthStatus.WARNING
        )

    def test_get_status_passing(self):
        self.run_get_status(
            True,
            {
                "four": True,
                "five": True,
            },
            HealthStatus.OK
        )

    def test_elasticsearch_unhealthy(self):
        self.run_get_status(
            False,
            {
                "four": True,
                "five": True,
            },
            HealthStatus.CRITICAL
        )
