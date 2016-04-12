from tests.functional_test_base import FunctionalTestBase
import pyshelf.bucket_update.utils as utils
import logging


class UtilsTest(FunctionalTestBase):
    def test_create_container(self):
        bucket_config = {
            "name": "my-test-bucket",
            "logLevel": logging.INFO
        }

        container = utils._create_container(bucket_config)
        logger = container.logger
        # There is not a whole lot else I can validate due
        # to the nature of basicConfig.  I do want to use
        # basicConfig though, so that other loggers in
        # third party tools will inherit the settings.
        self.assertEqual(bucket_config["name"], logger.name)
