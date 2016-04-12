from mock import Mock
from pyproctor import MonkeyPatcher
from tests.unit_test_base import UnitTestBase
import logging
import os.path
import pyshelf.bucket_update.utils as utils


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
