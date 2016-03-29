from mock import Mock
from pyshelf.search.container import Container as SearchContainer
import tests.metadata_utils as utils
from pyshelf.search.metadata import Metadata
import time


class TestWrapper(object):
    INIT = False

    def __init__(self):
        self.config = {
            "elasticSearchHost": ["localhost:9200"],
            "test": {
                "accessKey": "test",
                "secretKey": "test",
            }
        }
        self.logger = Mock()
        self._search_container = None

    def setup_metadata(self, name="test", path="test", version="1"):
        if not TestWrapper.INIT:
            Metadata.init()
            # Again temp fix for the above init request
            time.sleep(1)
            TestWrapper.INIT = True
        self.search_container.update_manager.update(name, utils.get_meta(name, path, version))

    def teardown_metadata(self, key):
        meta = self.search_container.update_manager.get_metadata(key)
        if meta:
            meta.delete()

    @property
    def search_container(self):
        if not self._search_container:
            self._search_container = SearchContainer(self.config, self.logger)

        return self._search_container
