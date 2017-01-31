from shelf.container import Container
from shelf.hook.manager import Manager as HookManager
from tests.test_base import TestBase
import logging


class ContainerTest(TestBase):
    def setUp(self):
        super(ContainerTest, self).setUp()
        self.app = type("FakeApp", (object, ), {
            "logger": logging.getLogger("ContainerTestLogger"),
            "config": {}
        })
        self.request = type("FakeRequest", (object, ), {
            "url": "https://api.shelf.com/blah/artifact/my/artifact"
        })
        self.container = Container(self.app, self.request)

    def test_hook_manager_with_hook_command(self):
        cmd = "/usr/local/bin/my-cmd"
        self.app.config["hookCommand"] = cmd
        manager = self.container.hook_manager
        self.assertIsInstance(manager, HookManager)
        self.assertEqual(cmd, manager.command)
        self.assertEqual("https://api.shelf.com", manager.host)
