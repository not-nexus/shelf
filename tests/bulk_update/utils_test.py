from tests.unit_test_base import UnitTestBase
from pyproctor import MonkeyPatcher
from mock import Mock
from pyshelf.bulk_update.runner import Runner
import os.path
from pyshelf.bulk_update.utils import run
import logging
from copy import deepcopy


class UtilsTest(UnitTestBase):
    EXPECTED_KYLE = {
        "chunkSize": 20,
        "name": "kyle-long",
        "logLevel": logging.INFO,
        "bulkUpdateLogDirectory": "/var/log/bucket-update",
        "elasticsearch": {
            "connectionString": "http://localhost:9200/metadata",
        },
        "accessKey": "KKKKKKKKKKKKKKKKKKKK",
        "secretKey": "KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK",
        "referenceName": "kyle-long"
    }

    EXPECTED_ANDY = {
        "chunkSize": 20,
        "name": "andy-gertjejansen",
        "logLevel": logging.INFO,
        "bulkUpdateLogDirectory": "/var/log/bucket-update",
        "elasticsearch": {
            "connectionString": "http://localhost:9200/metadata",
        },
        "accessKey": "AAAAAAAAAAAAAAAAAAAA",
        "secretKey": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
        "referenceName": "ag"
    }

    def setUp(self):
        super(UtilsTest, self).setUp()
        self.run_process_mock = Mock()
        MonkeyPatcher.patch(Runner, "_run_process", self.run_process_mock)

    def execute(self, bucket=None, chunk_size=20, verbose=False):
        path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../data/test_config.yaml")
        args = {
            "--chunk-size": chunk_size,
            "--bucket": bucket,
            "<config-path>": path,
            "--verbose": verbose
        }

        run(args)

    def run_and_assert_both_buckets(self, bucket):
        self.execute(bucket=bucket)
        self.assertEqual(2, self.run_process_mock.call_count)
        args_list = self.run_process_mock.call_args_list
        # I do this instead of assuming order since it is a dict
        # when the config is decoded and we can't rely on the
        # order of a dict
        for args in args_list:
            config = args[0][0]
            if config["name"] == "andy-gertjejansen":
                self.assertEqual(UtilsTest.EXPECTED_ANDY, config)
            else:
                self.assertEqual(UtilsTest.EXPECTED_KYLE, config)

    def test_run(self):
        self.run_and_assert_both_buckets(None)

    def test_with_comma_separated_bucket_list(self):
        self.run_and_assert_both_buckets("kyle-long, ag")

    def test_single_bucket_only(self):
        self.execute(bucket="kyle-long", verbose=True)
        self.assertEqual(1, self.run_process_mock.call_count)
        args = self.run_process_mock.call_args
        expected = deepcopy(UtilsTest.EXPECTED_KYLE)
        expected["logLevel"] = logging.DEBUG
        self.assertEqual(expected, args[0][0])
