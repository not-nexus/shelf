from tests.unit_test_base import UnitTestBase
import pyshelf.bucket_update.utils as utils
import logging
import os.path


class UtilsTest(UnitTestBase):
    def test_create_container(self):
        directory = os.path.dirname(os.path.realpath(__file__)) + "/../data/logging-dir"
        bucket_config = {
            "name": "my-test-bucket",
            "logLevel": logging.INFO,
            "bulkUpdateLogDirectory": directory
        }

        container = utils._create_container(bucket_config)
        logger = container.logger
        # There is not a whole lot else I can validate due
        # to the nature of basicConfig.  I do want to use
        # basicConfig though, so that other loggers in
        # third party tools will inherit the settings.
        self.assertEqual(bucket_config["name"], logger.name)
