import pyproctor
from mock import Mock, MagicMock
from pyshelf.search.container import Container as SearchContainer


class UnitTestBase(pyproctor.TestBase):
    def setUp(self):
        self.mock_container()
        self.search_container = SearchContainer(Mock(), "localhost:9200")

    def mock_container(self):
        request = Mock()
        self.container = Mock()
        self.container.request = request
        self.storage = Mock()
        self.storage.__exit__ = MagicMock(return_value=False)
        self.storage.__enter__ = MagicMock(return_value=self.storage)
        self.container.create_bucket_storage = MagicMock(return_value=self.storage)
