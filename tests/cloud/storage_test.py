from tests.test_base import TestBase
from pyshelf.cloud.storage import Storage
import logging


class StorageTest(TestBase):
    def setUp(self):
        logger = logging.Logger("StorageTest")
        self.storage = Storage("FakeAccessKey", "FakeSecretKey", "FakeBucketName", logger)

    def test_to_utc(self):
        date_string = "Wed, 18 May 2016 16:03:10 CDT"
        expected_string = "2016-05-18T21:03:10Z"
        new_date_string = self.storage._to_utc(date_string)
        self.assertEqual(expected_string, new_date_string)

    def test_to_utc_gmt(self):
        """
            This test exists because it looks like AWS
            will likely always return GMT but I am unable
            to confirm it.
        """
        date_string = "Wed, 18 May 2016 22:03:10 GMT"
        expected_string = "2016-05-18T22:03:10Z"
        new_date_string = self.storage._to_utc(date_string)
        self.assertEqual(expected_string, new_date_string)

    def test_unhandled_timezone(self):
        """
            RFC 822 only allows for some timezones.  Luckily
            the only one that is returned is supported (GMT).
            However, in the event we do get a different one
            back, we want to fail loudly so that we can put
            a fix into place.
        """
        date_string = "Wed, 18 May 2016 22:03:10 BST"
        with self.assertRaises(ValueError):
            self.storage._to_utc(date_string)
