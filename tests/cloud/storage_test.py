from tests.test_base import TestBase
from pyshelf.cloud.storage import Storage
import logging


class StorageTest(TestBase):
    def setUp(self):
        logger = logging.Logger("StorageTest")
        self.storage = Storage("FakeAccessKey", "FakeSecretKey", "FakeBucketName", logger)

    def test_travis_ci(self):
        from datetime import datetime

        date_string = "Wed, 18 May 2016 16:03:10 CST"
        datetime.strptime(date_string, "%a, %d %b %Y %X %Z")

    #  def test_to_utc(self):
    #      date_string = "Wed, 18 May 2016 16:03:10 CST"
    #      expected_string = "2016-05-18T21:03:10Z"
    #      new_date_string = self.storage._to_utc(date_string)
    #      self.assertEqual(expected_string, new_date_string)

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
