from tests.test_base import TestBase
from pyshelf.health import Health

class HealthTest(TestBase):
    def test_get_failing_ref_name_list(self):
        health = Health()

        health.refNames = {
            "hi": False,
            "hello": True,
            "other": False,
        }

        expected = [
            "hi",
            "other"
        ]

        actual = health.get_failing_ref_name_list()
        # I sort them because the order in which dictionaries will iterate
        # through items is not reliable by design.
        self.assertEqual(sorted(expected), sorted(actual))
