from tests.unit_test_base import UnitTestBase
from pyproctor import MonkeyPatcher
from mock import Mock
from pyshelf.bulk_update.runner import Runner
import os.path
from pyshelf.bulk_update.utils import run
import logging


class UtilsTest(UnitTestBase):
    EXPECTED_KYLE = {
        "chunkSize": 20,
        "name": "kyle-long",
        "logLevel": logging.INFO,
        "elasticSearchConnectionString": "http://localhost:9200/metadata",
        "accessKey": "KKKKKKKKKKKKKKKKKKKK",
        "secretKey": "KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK"
    }

    EXPECTED_ANDY = {
        "chunkSize": 20,
        "name": "andy-gertjejansen",
        "logLevel": logging.INFO,
        "elasticSearchConnectionString": "http://localhost:9200/metadata",
        "accessKey": "AAAAAAAAAAAAAAAAAAAA",
        "secretKey": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    }

    def setUp(self):
        super(UtilsTest, self).setUp()
        self.run_process_mock = Mock()
        MonkeyPatcher.patch(Runner, "_run_process", self.run_process_mock)

    def execute(self, bucket=None, chunk_size=None):
        path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../data/test_config.yaml")
        args = {
            "--chunk-size": 20,
            "--bucket": bucket,
            "<config-path>": path,
            "--verbose": False
        }

        if chunk_size:
            args["--chunk-size"] = chunk_size

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
        self.run_and_assert_both_buckets("kyle-long, andy-gertjejansen")

    def test_single_bucket_only(self):
        self.execute(bucket="kyle-long")
        self.assertEqual(1, self.run_process_mock.call_count)
        args = self.run_process_mock.args
        self.assertEqual(UtilsTest.EXPECTED_KYLE, args[0][0])
