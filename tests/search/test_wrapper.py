from pyshelf.search.metadata import Metadata
import time


class TestWrapper(object):
    INIT = False

    def __init__(self, search_container):
        self.search_container = search_container
        self.doc_list = []
        self.es = self.search_container.elastic_search

    def setup_metadata(self, data):
        if not TestWrapper.INIT:
            Metadata.init(using=self.search_container.elastic_search)
            Metadata._doc_type.refresh(using=self.es)
            time.sleep(.5)
            TestWrapper.INIT = True
        for doc in data:
            self.doc_list.append(doc["artifactName"]["value"])
            meta = Metadata()
            meta.meta.id = doc["artifactName"]["value"]
            meta.update_all(doc)
            meta.save(using=self.es)

    def teardown_metadata(self):
        for key in self.doc_list:
            meta = self.get_metadata(key)
            print meta
            if meta:
                meta.delete(using=self.es)

        self.doc_list = []

    def get_metadata(self, id):
        return Metadata.get(using=self.es, id=id, ignore=404)
