from shelf.search.metadata import Metadata


class TestWrapper(object):
    INIT = False

    def __init__(self, search_container):
        self.search_container = search_container
        self.connection = self.search_container.connection
        self.index = self.search_container.connection.es_index

    def setup_metadata(self, data):
        for doc in data:
            self.add_metadata(doc["artifactName"]["value"], doc)

        self.refresh_index()

    def add_metadata(self, key, metadata):
        self.init_metadata()
        meta = Metadata()
        meta.meta.id = key
        meta.meta.index = self.index
        meta.update_all(metadata)
        meta.save(using=self.connection)

    def refresh_index(self):
        self.connection.indices.refresh(index=self.index)

    def teardown_metadata(self):
        self.search_container.update_manager.remove_unlisted_documents([])

    def init_metadata(self):
        if not TestWrapper.INIT:
            # This is necessary as I added an analyzer with a keyword tokenizer
            # which requires an index to be closed and reopened.
            self.connection.indices.delete(index=self.index, ignore=404)
            Metadata.init(index=self.index, using=self.connection)
            self.connection.indices.refresh(index=self.index)
            TestWrapper.INIT = True

    def get_metadata(self, id):
        return Metadata.get(index=self.index, using=self.connection, id=id, ignore=404)
