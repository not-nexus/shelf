from pyshelf.search.metadata import Metadata
from elasticsearch import Elasticsearch


class TestWrapper(object):
    INIT = False

    def __init__(self, search_container):
        self.search_container = search_container
        self.es = Elasticsearch(self.search_container.es_url)
        self.index = self.search_container.es_index

    def setup_metadata(self, data):
        self.init_metadata()
        for doc in data:
            meta = Metadata()
            meta.meta.id = doc["artifactName"]["value"]
            meta.meta.index = self.index
            meta.update_all(doc)
            meta.save(using=self.es)

        self.es.indices.refresh(index=self.index)

    def teardown_metadata(self):
        self.search_container.update_manager.remove_unlisted_documents([])

    def init_metadata(self):
        if not TestWrapper.INIT:
            Metadata.init(index=self.index, using=self.es)
            self.es.indices.refresh(index=self.index)
            TestWrapper.INIT = True

    def get_metadata(self, id):
        return Metadata.get(index=self.index, using=self.es, id=id, ignore=404)
