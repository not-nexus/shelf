from mock import Mock
from pyproctor import MonkeyPatcher
from shelf.bucket_update.utils import update_search_index
from shelf.bulk_update.runner import Runner
from tests.unit_test_base import UnitTestBase
import multiprocessing


class RunnerTest(UnitTestBase):
    """
        This test only exists for things that are not tested
        more functionally in the tests.bulk_update.utils_test.UtilsTest
    """
    def setUp(self):
        super(RunnerTest, self).setUp()
        self.fake_process = type("FakeProcess", (object,), {})()
        self.fake_process = Mock()
        self.fake_container = type("FakeContainer", (object,), {})()
        self.fake_container.config = {}
        self.fake_process_constructor = Mock(return_value=self.fake_process)
        MonkeyPatcher.patch(multiprocessing, "Process", self.fake_process_constructor)
        self.runner = Runner(self.fake_container, update_search_index)

    def test_run_process(self):
        fake_config = {
            "blah": "blah"
        }
        self.runner._run_process(fake_config)
        self.fake_process_constructor.assert_called_with(
            target=update_search_index,
            args=(fake_config,)
        )

        self.assertTrue(self.fake_process.start.called)
