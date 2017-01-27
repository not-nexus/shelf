from tests.test_base import TestBase
from shelf.hook.background import action
import logging


class ActionTest(TestBase):
    def test_create_background_logger(self):
        logger = action.create_background_logger(logging.DEBUG)
        self.assertIsInstance(logger, logging.Logger)
        self.assertEqual(logging.DEBUG, logger.level)
