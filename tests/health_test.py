from tests.test_base import TestBase
from pyshelf.health import Health


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
            "other"
        ]

        actual = self.health.get_passing_ref_name_list()
        self.assertEqual(sorted(expected), sorted(actual))
