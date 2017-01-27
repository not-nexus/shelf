from mock import Mock
from shelf.hook.background import action
from shelf.hook.event import Event
from tests.test_base import TestBase
import json
import os
import logging


class ExecuteCommandTest(TestBase):

    def setUp(self):
        super(ExecuteCommandTest, self).setUp()
        self.cwd = os.path.join(os.path.dirname(__file__), "../../..")
        self.logger = Mock()

        action.create_background_logger = Mock(return_value=self.logger)

    def create_data(self, command, event):
        data = {
            "command": command,
            "log_level": logging.DEBUG,
            "event": event,
            "uri": "https://api.shelf.com/fake/artifact/1",
            "meta_uri": "https://api.shelf.com/fake/artifact/1/_meta",
            "cwd": self.cwd
        }

        return data

    def create_stdout(self, data):
        l = [
            "SHELF_EVENT={0}".format(data["event"]),
            "SHELF_URI={0}".format(data["uri"]),
            "SHELF_META_URI={0}".format(data["meta_uri"])
        ]

        return ", ".join(l)

    def test_success(self):
        data = self.create_data("./tests/bin/hook-test", Event.ARTIFACT_UPLOADED)
        result = action.execute_command(**data)
        self.assertTrue(result)

        expected_result = {
            "stdout": self.create_stdout(data),
            "stderr": "STDERR",
            "exit_code": 0
        }

        self.logger.debug.assert_called_with("Command Result: {0}".format(json.dumps(expected_result, indent=4)))

    def test_failure(self):
        data = self.create_data("./tests/bin/hook-test", "fail")
        result = action.execute_command(**data)
        self.assertFalse(result)

        expected_result = {
            "stdout": self.create_stdout(data),
            "stderr": "STDERR",
            "exit_code": 1
        }

        self.logger.debug.assert_called_with("Command Result: {0}".format(json.dumps(expected_result, indent=4)))
