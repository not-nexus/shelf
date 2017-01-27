from mock import Mock
from shelf.hook.background import action
from shelf.hook.container import Container
from shelf.hook.event import Event
from shelf.hook.manager import Manager
from shelf.resource_identity import ResourceIdentity
from tests.test_base import TestBase
import logging


class ManagerTest(TestBase):
    def setUp(self):
        super(ManagerTest, self).setUp()
        self.process = Mock()
        self.multiprocessing = type("FakeMultiprocessing", (object, ), {
            "Process": Mock(return_value=self.process)
        })

        self.identity = ResourceIdentity("/blah/artifact/my/path")
        self.command = "/usr/local/bin/my-cmd"
        self.host = "https://api.shelf.com"
        self.logger = logging.getLogger("TestLogger")
        self.logger.setLevel(logging.INFO)
        self.container = Container(self.logger)
        self.manager = Manager(
            self.container,
            self.multiprocessing,
            self.host,
            self.command
        )

    def assert_process(self, event):
        self.multiprocessing.Process.assert_called_with(
            target=action.execute_command,
            kwargs={
                "command": self.command,
                "event": event,
                "uri": "https://api.shelf.com/blah/artifact/my/path",
                "meta_uri": "https://api.shelf.com/blah/artifact/my/path/_meta",
                "log_level": logging.INFO
            }
        )

        self.process.start.assert_called_once_with()

    def test_notify_artifact_uploaded(self):
        self.manager.notify_artifact_uploaded(self.identity)
        self.assert_process(Event.ARTIFACT_UPLOADED)

    def test_notify_metadata_updated(self):
        self.manager.notify_metadata_updated(self.identity)
        self.assert_process(Event.METADATA_UPDATED)
