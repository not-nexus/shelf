from mock import Mock
from pyshelf.search.container import Container as SearchContainer
import tests.metadata_utils as utils
from pyshelf.search.metadata import Metadata
import time


class TestWrapper(object):
    INIT = False

    def __init__(self):
        self.elastic_search_host = "localhost:9200"
        self.logger = Mock()
        self._search_container = None

    def setup_metadata(self, name="test", path="test", version="1"):
        if not TestWrapper.INIT:
            Metadata.init(using=self.search_container.elastic_search)
            # Again temp fix for the above init request
            time.sleep(1)
            TestWrapper.INIT = True
        self.search_container.update_manager.update(name, utils.get_meta(name, path, version))

    def teardown_metadata(self, key):
        meta = self.search_container.update_manager.get_metadata(key)
        if meta:
            meta.delete(using=self.search_container.elastic_search)

    @property
    def search_container(self):
        if not self._search_container:
            self._search_container = SearchContainer(self.logger, self.elastic_search_host)

        return self._search_container
