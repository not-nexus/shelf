from tests.unit_test_base import UnitTestBase
from pyproctor import MonkeyPatcher
from mock import Mock
from pyshelf.bulk_update.runner import Runner
import os.path
from pyshelf.bulk_update.utils import run


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
