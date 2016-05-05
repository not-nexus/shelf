from mock import Mock
from pyproctor import MonkeyPatcher
from tests.unit_test_base import UnitTestBase
import logging
import os.path
import pyshelf.bucket_update.utils as utils
from pyshelf import background_utils
from pyshelf.bucket_update.container import Container
import os
import glob


class UtilsTest(UnitTestBase):
    def setUp(self):
        super(UtilsTest, self).setUp()
        self.directory = os.path.dirname(os.path.realpath(__file__)) + "/../data/logging-dir"

    def tearDown(self):
        super(UtilsTest, self).tearDown()
        file_list = glob.glob(self.directory + "/*")
        for f in file_list:
            os.remove(f)

    def test_create_container(self):
        configure_file_logger = self.mock_configure_logger()
        bucket_config = {
            "name": "my-test-bucket",
            "logLevel": logging.INFO,
            "bulkUpdateLogDirectory": self.directory,
            "elasticsearch": self.config,
            "referenceName": "test"
        }

        container = utils._create_container(bucket_config)
        self.assertIsInstance(container, Container)

        arg_list = configure_file_logger.call_args_list
        first = arg_list[0][0]
        second = arg_list[1][0]
        log_file = self.directory + "/my-test-bucket.log"
        self.assertEqual(("elasticsearch", log_file, logging.INFO), first)
        self.assertEqual(("my-test-bucket", log_file, logging.INFO), second)

    def mock_configure_logger(self):
        logger = logging.getLogger()
        configure_file_logger = Mock(return_value=logger)
        MonkeyPatcher.patch(background_utils, "configure_file_logger", configure_file_logger)
        return configure_file_logger

    def test_update_search_index(self):
        container = type("FakeContainer", (object,), {})()
        container.search_updater = type("FakeSearchUpdater", (object,), {})()
        container.search_updater.run = Mock()
        _create_container = Mock(return_value=container)
        MonkeyPatcher.patch(utils, "_create_container", _create_container)
        fake_config = {"fake": "blah"}
        utils.update_search_index(fake_config)
        _create_container.assert_called_with(fake_config)
        self.assertTrue(container.search_updater.run.called)

    def test_configure_logger(self):
        logger = background_utils.configure_file_logger("super-unique-name", self.directory + "/lol.log", logging.DEBUG)
        handler = logger.handlers[0]
        self.assertIsInstance(handler, logging.FileHandler)
        self.assertEqual("super-unique-name", logger.name)
