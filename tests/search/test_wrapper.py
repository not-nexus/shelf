from mock import Mock
from pyshelf.search.container import Container as SearchContainer
import tests.metadata_utils as utils
from pyshelf.search.metadata import Metadata
from pyshelf.search.manager import Manager as SearchManager
from pyshelf.search.update_manager import UpdateManager


class TestWrapper(object):
    def __init__(self):
        self.config = {
            "elasticSearchHost": ["localhost:9200"],
            "test": {
                "accessKey": "test",
                "secretKey": "test",
            }
        }
        self.logger = Mock()
        self._update_manager = None
        self._search_manager = None
        self._search_container = None

    def setup_metadata(self, name="test", path="test", version="1"):
        Metadata.init()
        self.update_manager.update(name, utils.get_meta(name, path, version))

    def teardown_metadata(self, key):
        meta = self.update_manager.get_metadata(key)
        if meta:
            meta.delete()

    @property
    def update_manager(self):
        if not self._update_manager:
            self._update_manager = UpdateManager(self.search_container)

        return self._update_manager

    @property
    def search_manager(self):
        if not self._search_manager:
            self._search_manager = SearchManager(self.search_container)

        return self._search_manager

    @property
    def search_container(self):
        if not self._search_container:
            self._search_container = SearchContainer(self.logger, self.config)

        return self._search_container
