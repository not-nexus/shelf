import tests.metadata_utils as utils
from pyshelf.search.metadata import Metadata
import time


class TestWrapper(object):
    INIT = False

    def __init__(self, search_container):
        self.search_container = search_container

    def setup_metadata(self, name="test", path="test", version="1"):
        if not TestWrapper.INIT:
            Metadata.init(using=self.search_container.elastic_search)
            Metadata._doc_type.refresh(using=self.search_container.elastic_search)
            time.sleep(.5)
            TestWrapper.INIT = True
        self.search_container.update_manager.update(name, utils.get_meta(name, path, version))

    def teardown_metadata(self, key):
        meta = self.search_container.update_manager._get_metadata(key)
        if meta:
            meta.delete(using=self.search_container.elastic_search)
