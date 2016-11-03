from tests.unit_test_base import UnitTestBase
from shelf.metadata.initializer import Initializer


class InitializerTest(UnitTestBase):
    def test_get_created_date(self):
        """
            A rather weak test.  It exists mostly to
            make sure it doesn't blow up.
        """
        fake_container = type('FakeContainer', (object,), {})()
        fake_container.mapper = type('FakeMapper', (object,), {})()
        i = Initializer(fake_container)
        date = i._get_created_date()
        self.assertIsInstance(date, basestring)
