from tests.unit_test_base import UnitTestBase
from pyproctor import MonkeyPatcher
from mock import Mock
from pyshelf.bulk_update.runner import Runner
import os.path
from pyshelf.bulk_update.utils import run
import logging


class UtilsTest(UnitTestBase):
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

    def test_run(self):
        self.execute()
        self.assertEqual(2, self.run_process_mock.call_count)
        args_list = self.run_process_mock.call_args_list
        expected_kyle = {
            "chunkSize": 20,
            "name": "kyle-long",
            "logLevel": logging.INFO,
            "elasticSearchConnectionString": "http://localhost:9200/metadata",
            "accessKey": "KKKKKKKKKKKKKKKKKKKK",
            "secretKey": "KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK"
        }

        expected_andy = {
            "chunkSize": 20,
            "name": "andy-gertjejansen",
            "logLevel": logging.INFO,
            "elasticSearchConnectionString": "http://localhost:9200/metadata",
            "accessKey": "AAAAAAAAAAAAAAAAAAAA",
            "secretKey": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        }

        for args in args_list:
            config = args[0][0]
            if config["name"] == "andy-gertjejansen":
                self.assertEqual(expected_andy, config)
            else:
                self.assertEqual(expected_kyle, config)
