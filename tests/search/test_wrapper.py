from pyshelf.search.metadata import Metadata
from elasticsearch import Elasticsearch


class TestWrapper(object):
    INIT = False

    def __init__(self, search_container):
        self.search_container = search_container
        self.doc_list = []
        self.es = Elasticsearch(self.search_container.es_url)
        self.index = self.search_container.es_index

    def setup_metadata(self, data):
        for doc in data:
            self.doc_list.append(doc["artifactName"]["value"])
            self.add_metadata(doc["artifactName"]["value"], doc)

    def add_metadata(self, key, metadata):
        self.init_metadata()
        meta = Metadata()
        meta.meta.id = key
        meta.meta.index = self.index
        meta.update_all(metadata)
        meta.save(using=self.es)
        self.es.indices.refresh(index=self.index)

    def teardown_metadata(self):
        for key in self.doc_list:
            meta = self.get_metadata(key)
            if meta:
                meta.delete(using=self.es)

        self.doc_list = []

    def init_metadata(self):
        if not TestWrapper.INIT:
            Metadata.init(index=self.index, using=self.es)
            self.es.indices.refresh(index=self.index)
            TestWrapper.INIT = True


    def delete_all_metadata(self):
        self.search_container.update_manager.remove_unlisted_documents([])

    def get_metadata(self, id):
        return Metadata.get(index=self.index, using=self.es, id=id, ignore=404)
